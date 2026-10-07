import unittest
from shop import orders
from shop.orders import Order, OrderService


def make(pm="card", ship="standard", country="BR", vip=False, items=None):
    items = items or [{"sku": "A", "price": 100, "qty": 2, "category": "toys"}]
    return Order(1, {"name": "Ana", "email": "a@x.com", "phone": "119", "vip": vip}, items, pm, ship, country)


class T(unittest.TestCase):
    def setUp(self):
        orders.SENT_EMAILS.clear(); orders.SENT_SMS.clear(); orders.ANALYTICS.clear()

    def test_card_standard(self):
        o = OrderService().process_order(make(), card_token="tok_1234")
        self.assertEqual(o.total, 230.0)
        self.assertEqual(o.payment_ref, "CARD-1234")
        self.assertEqual(o.status, "paid")
        self.assertEqual(len(orders.SENT_SMS), 1)

    def test_vip_books_weekend_express(self):
        o = OrderService().process_order(make(pm="pix", ship="express", vip=True,
            items=[{"sku": "B", "price": 600, "qty": 1, "category": "books"}]), day="sun")
        self.assertEqual(o.total, round(600 - (60 + 20 + 5 + 12) + 25 + (600 - 97) * 0.1, 2))

    def test_boleto_limit(self):
        with self.assertRaises(ValueError):
            OrderService().process_order(make(pm="boleto", items=[{"sku": "C", "price": 6000, "qty": 1, "category": "x"}]))

    def test_legacy(self):
        o = OrderService().process_order(make(pm="legacy_card", ship="pickup"), card_token="t")
        self.assertEqual(o.payment_ref, "LP-1")

    def test_lifecycle(self):
        s = OrderService()
        o = s.process_order(make(pm="pix"))
        s.advance(o, "ship"); s.advance(o, "return")
        self.assertEqual(o.status, "returned")
        self.assertIn(("refund", 1, o.total), orders.ANALYTICS)
        with self.assertRaises(ValueError):
            s.advance(o, "ship")


if __name__ == "__main__":
    unittest.main()
