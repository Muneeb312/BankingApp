"""
transactions.py
---------------
Intention: Handles financial transactions (deposit, withdraw, transfer).
"""

class Transactions:
    def __init__(self, file_handler, session_manager):
        self.file_handler = file_handler
        self.session = session_manager
        self.amount = 0
        self.account_number = 0
        self.receiver_account_number = 0

    def deposit(self, account_num, amount):
        self.account_number = account_num
        self.amount = amount
        self.file_handler.write_transaction(f"04 {account_num} {amount} 00000 **")
        print(f"Deposited {amount} to {account_num}.")

    def withdrawal(self, account_num, amount):
        self.account_number = account_num
        self.amount = amount
        self.file_handler.write_transaction(f"01 {account_num} {amount} 00000 **")
        print(f"Withdrawn {amount} from {account_num}.")

    def transfer(self, from_account, to_account, amount):
        self.account_number = from_account
        self.receiver_account_number = to_account
        self.amount = amount
        self.file_handler.write_transaction(f"02 {from_account} {to_account} {amount} **")
        print(f"Transferred {amount} from {from_account} to {to_account}.")

    def paybill(self, account_num, amount, company):
        self.account_number = account_num
        self.amount = amount
        self.file_handler.write_transaction(f"03 {account_num} {amount} {company} **")
        print(f"Bill paid: {amount} to {company} from {account_num}.")