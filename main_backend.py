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

    accounts = [acc for acc in accounts if "END_OF_FILE" not in acc['name']]
    for trans_line in transactions:
        parts = trans_line.split()
        if not parts:
            continue

        trans_code = parts[0]

        # Session commands (Login 10, Logout 00) don't change balances
        if trans_code in ["10", "00"]:
            continue

        # Example: Processing a Deposit (04)
            # Withdrawals (01)
        elif trans_code == "01":
            account_num = parts[1].lstrip('0') or '0'
            amount = float(parts[2])
            for acc in accounts:
                if acc['account_number'] == account_num:
                    acc['balance'] -= amount
                    acc['total_transactions'] += 1
                    break

        # Transfers (02)
        elif trans_code == "02":
            from_acc = parts[1].lstrip('0') or '0'
            amount = float(parts[2])
            to_acc = parts[3].lstrip('0') or '0'
            # Deduct from first account
            for acc in accounts:
                if acc['account_number'] == from_acc:
                    acc['balance'] -= amount
                    acc['total_transactions'] += 1
                    break
            # Add to second account
            for acc in accounts:
                if acc['account_number'] == to_acc:
                    acc['balance'] += amount
                    acc['total_transactions'] += 1
                    break

        # Deposits (04)
        elif trans_code == "04":
            account_num = parts[1].lstrip('0') or '0'
            amount = float(parts[2])
            for acc in accounts:
                if acc['account_number'] == account_num:
                    acc['balance'] += amount
                    acc['total_transactions'] += 1
                    break

        # Create Account (05)
        elif trans_code == "05":
            # INTEGRATION FIX: The Front End puts the Name BEFORE the Account Number.
            # We will scan the line to find the first pure number and use that as the ID.
            acc_index = 2  # Default assumption
            for i in range(1, len(parts)):
                if parts[i].isdigit():
                    acc_index = i
                    break

            name = " ".join(parts[1:acc_index])  # Everything before the number is the name
            account_num = parts[acc_index].lstrip('0') or '0'

            new_account = {
                'account_number': account_num,
                'name': name,
                'status': 'A',
                'balance': 0.0,
                'total_transactions': 0,
                'plan': 'NP'
            }
            accounts.append(new_account)
        # Delete Account (06)
        elif trans_code == "06":
            account_num = parts[1].lstrip('0') or '0'
            accounts = [acc for acc in accounts if acc['account_number'] != account_num]

        # Disable Account (07)
        elif trans_code == "07":
            account_num = parts[1].lstrip('0') or '0'
            for acc in accounts:
                if acc['account_number'] == account_num:
                    acc['status'] = 'D'
                    break

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