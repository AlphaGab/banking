class BankUser:
    def __init__(self, customer_name="none", account_type="none", pin_number="none", balance='0',card_number=0):
        self.customer_name = customer_name
        self.account_type = account_type
        self.pin_number = pin_number
        self.balance = balance
        self.card_number = card_number