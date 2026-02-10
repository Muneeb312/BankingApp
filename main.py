import sys
from SessionManager import SessionManager
from AccountManager import AccountManager   
from Transactions import Transactions
# from Account import account

"""
main.py
-------
Intention: Entry point for the Banking System. It initializes the FileHandler,
instantiates the managers, and runs the main Read-Eval-Print Loop (REPL).
"""

class FileHandler:
    """
    Handles reading the valid accounts file and writing to the daily transaction file.
    Passed to all other managers so they can save their data.
    """
    def __init__(self, accounts_path, output_path):
        self.valid_accounts = self.load_accounts(accounts_path)
        self.output_path = output_path

    def load_accounts(self, path):
        try:
            with open(path, 'r') as f:
                # Returns a list of strings, e.g., ['12345', '99999']
                return [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print(f"Error: Accounts file '{path}' not found.")
            sys.exit(1)

    def write_transaction(self, transaction_code):
        try:
            with open(self.output_path, 'a') as f:
                f.write(transaction_code + '\n')
        except IOError:
            print(f"Error: Could not write to output file '{self.output_path}'.")

def main():
    # 1. Check Command Line Arguments
    if len(sys.argv) != 3:
        print("Usage: python main.py <valid_accounts_list_file> <transaction_output_file>")
        sys.exit(1)

    accounts_file = sys.argv[1]
    output_file = sys.argv[2]

    # 2. Initialize the Helper and Managers
    file_handler = FileHandler(accounts_file, output_file)
    
    # Session Manager handles Login/Logout state
    session_mgr = SessionManager(file_handler)
    
    # Account Manager handles Admin tasks (Create, Delete, etc.)
    # We pass session_mgr so it can check if the user is an Admin
    account_mgr = AccountManager(file_handler, session_mgr)
    
    # Transactions handles Financial tasks (Deposit, Withdraw, etc.)
    transaction_mgr = Transactions(file_handler, session_mgr)

    print("Welcome to the Banking System.")
    print("Type 'login admin' or 'login standard' to begin.")

    # 3. Main Input Loop
    try:
        for line in sys.stdin:
            parts = line.strip().split()
            if not parts:
                continue
            
            command = parts[0]

            # --- Session Commands ---
            if command == "login":
                if len(parts) > 1:
                    session_mgr.login(parts[1])
                else:
                    print("Usage: login [standard|admin]")
            
            elif command == "logout":
                session_mgr.logout()

            # --- Check Login State ---
            # If not logged in, no other commands are allowed
            elif not session_mgr.isLoggedIn:
                print("Error: You must login first.")

            # --- Account Manager Commands (Admin) ---
            elif command in ["create", "delete", "disable", "changeplan"]:
                if len(parts) >= 3:
                    if command == "create": 
                        account_mgr.create(parts[1], parts[2])
                    elif command == "delete": 
                        account_mgr.delete(parts[1], parts[2])
                    elif command == "disable": 
                        account_mgr.disable(parts[1], parts[2])
                    elif command == "changeplan": 
                        account_mgr.changeplan(parts[1], parts[2])
                else:
                    print(f"Usage: {command} <account_num> <account_name>")

            # --- Transaction Commands (Financial) ---
            elif command in ["deposit", "withdrawal", "transfer", "paybill"]:
                if command == "deposit" and len(parts) == 3:
                    transaction_mgr.deposit(parts[1], parts[2])
                
                elif command == "withdrawal" and len(parts) == 3:
                    transaction_mgr.withdrawal(parts[1], parts[2])
                
                elif command == "transfer" and len(parts) == 4:
                    transaction_mgr.transfer(parts[1], parts[2], parts[3])
                
                elif command == "paybill" and len(parts) == 4:
                    transaction_mgr.paybill(parts[1], parts[2], parts[3])
                
                else:
                    print(f"Invalid arguments for {command}.")

            else:
                print("Error: Unknown command.")

    except KeyboardInterrupt:
        print("\nForce Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()