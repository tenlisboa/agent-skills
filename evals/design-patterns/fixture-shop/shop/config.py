class Config:
    _instance = None

    def __init__(self):
        self.tax_rate = 0.1
        self.smtp_host = "smtp.example.com"
        self.legacy_payments_key = "test-key"

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = Config()
        return cls._instance
