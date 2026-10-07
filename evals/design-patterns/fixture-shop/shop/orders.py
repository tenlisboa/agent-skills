from shop.config import Config
from shop.legacy_pay import LegacyPayClient

SENT_EMAILS = []
SENT_SMS = []
ANALYTICS = []


class Order:
    def __init__(self, id, customer, items, payment_method, shipping, country):
        self.id = id
        self.customer = customer  # dict: name, email, phone, vip
        self.items = items  # list of dicts: sku, price, qty, category
        self.payment_method = payment_method  # "card", "pix", "boleto", "legacy_card"
        self.shipping = shipping  # "standard", "express", "pickup"
        self.country = country
        self.status = "new"
        self.total = 0
        self.payment_ref = None


def is_weekend(day):
    if day in ("sat", "sun"):
        return True
    return False


class OrderService:
    def __init__(self):
        self.legacy = LegacyPayClient(Config.get().legacy_payments_key)

    def process_order(self, order, card_token=None, day="mon"):
        # subtotal
        subtotal = 0
        for it in order.items:
            subtotal += it["price"] * it["qty"]
        # discounts
        discount = 0
        if order.customer.get("vip"):
            discount += subtotal * 0.1
        if subtotal > 500:
            discount += 20
        if any(it["category"] == "books" for it in order.items) and order.country == "BR":
            discount += 5
        if is_weekend(day):
            discount += subtotal * 0.02
        # shipping
        if order.shipping == "standard":
            shipping_cost = 10 if order.country == "BR" else 30
        elif order.shipping == "express":
            shipping_cost = 25 if order.country == "BR" else 60
        elif order.shipping == "pickup":
            shipping_cost = 0
        else:
            raise ValueError("unknown shipping")
        tax = (subtotal - discount) * Config.get().tax_rate
        order.total = round(subtotal - discount + shipping_cost + tax, 2)
        # payment
        if order.payment_method == "card":
            if not card_token:
                raise ValueError("card token required")
            order.payment_ref = "CARD-" + card_token[-4:]
        elif order.payment_method == "pix":
            order.payment_ref = "PIX-" + str(order.id)
        elif order.payment_method == "boleto":
            if order.total > 5000:
                raise ValueError("boleto limit")
            order.payment_ref = "BOL-" + str(order.id)
        elif order.payment_method == "legacy_card":
            res = self.legacy.doTransaction(int(order.total * 100), "BRL", card_token)
            if res["status_code"] != "00":
                raise RuntimeError("legacy payment failed")
            order.payment_ref = res["ref"]
        else:
            raise ValueError("unknown payment")
        order.status = "paid"
        # notifications
        SENT_EMAILS.append((order.customer["email"], "Order %s paid" % order.id))
        if order.customer.get("phone"):
            SENT_SMS.append((order.customer["phone"], "Order %s paid" % order.id))
        ANALYTICS.append(("order_paid", order.id, order.total))
        return order

    def advance(self, order, action):
        if order.status == "paid":
            if action == "ship":
                order.status = "shipped"
            elif action == "cancel":
                order.status = "cancelled"
                ANALYTICS.append(("refund", order.id, order.total))
            else:
                raise ValueError("invalid action %s in paid" % action)
        elif order.status == "shipped":
            if action == "deliver":
                order.status = "delivered"
            elif action == "return":
                order.status = "returned"
                ANALYTICS.append(("refund", order.id, order.total))
            else:
                raise ValueError("invalid action %s in shipped" % action)
        elif order.status in ("delivered", "cancelled", "returned"):
            raise ValueError("order %s is final" % order.id)
        elif order.status == "new":
            raise ValueError("order not paid")
        SENT_EMAILS.append((order.customer["email"], "Order %s is %s" % (order.id, order.status)))
        return order
