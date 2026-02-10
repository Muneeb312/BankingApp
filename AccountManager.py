"""
account_manager.py
------------------
Intention: Handles administrative account maintenance (create, delete, etc).
"""

class AccountManager:
    def __init__(self, file_handler, session_manager):
        self.file_handler = file_handler
        self.session = session_manager
        self.account_number = 0
        self.account_status = False
        self.account_type = ""
        self.account_plan = ""

    def create(self, account_num, name):
        if not self.session.isAdmin:
            print("Error: Privilege Denied. Admin only.")
            return
        self.account_number = account_num
        self.file_handler.write_transaction(f"05 {name} {account_num} 00000 **")
        print(f"Account {account_num} created.")

    def delete(self, account_num, name):
        if not self.session.isAdmin:
            print("Error: Privilege Denied. Admin only.")
            return
        self.account_number = account_num
        self.file_handler.write_transaction(f"06 {name} {account_num} 00000 **")
        print(f"Account {account_num} deleted.")

    def disable(self, account_num, name):
        if not self.session.isAdmin:
            print("Error: Privilege Denied. Admin only.")
            return
        self.file_handler.write_transaction(f"07 {name} {account_num} 00000 **")
        print(f"Account {account_num} disabled.")

    def changeplan(self, account_num, name):
        if not self.session.isAdmin:
            print("Error: Privilege Denied. Admin only.")
            return
        self.file_handler.write_transaction(f"08 {name} {account_num} 00000 **")
        print(f"Plan changed for account {account_num}.")