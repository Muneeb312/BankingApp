import sys
from read import read_old_bank_accounts
from write import write_new_current_accounts
from print_error import log_constraint_error


def process_transactions(accounts, transaction_file_path):
    """
    Reads the daily transaction file and routes each transaction
    to update the correct account's balance or status.
    """
    try:
        with open(transaction_file_path, 'r') as file:
            transactions = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        log_constraint_error("Transaction file not found.", transaction_file_path, fatal=True)
        return accounts

    for trans_line in transactions:
        parts = trans_line.split()
        if not parts:
            continue

        trans_code = parts[0]

        # Session commands (Login 10, Logout 00) don't change balances
        if trans_code in ["10", "00"]:
            continue

        # Example: Processing a Deposit (04)
        elif trans_code == "04":
            # Strip leading zeros from the account number to match the dictionary
            account_num = parts[1].lstrip('0') or '0'
            amount = float(parts[2])

            for acc in accounts:
                if acc['account_number'] == account_num:
                    acc['balance'] += amount
                    acc['total_transactions'] += 1
                    break


    return accounts


def main():
    """
    The entry point method that parses command-line arguments
    and drives the batch processing lifecycle.
    """
    # Ensures the correct number of files are provided in the terminal
    if len(sys.argv) != 4:
        print("Usage: python main_backend.py <old_master.txt> <daily_transactions.etf> <new_master.txt>")
        sys.exit(1)

    old_master_path = sys.argv[1]
    transaction_path = sys.argv[2]
    new_master_path = sys.argv[3]

    print("[*] Reading Old Master Accounts...")
    current_accounts = read_old_bank_accounts(old_master_path)

    print("[*] Processing Transactions...")
    updated_accounts = process_transactions(current_accounts, transaction_path)

    print("[*] Writing New Master Accounts...")
    write_new_current_accounts(updated_accounts, new_master_path)

    print("[+] Backend Batch Processing Complete.")


if __name__ == "__main__":
    main()