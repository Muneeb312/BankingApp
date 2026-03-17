import pytest
import os
from write import write_new_current_accounts
from main_backend import process_transactions

@pytest.fixture
def base_account():
    """Provides account for statement coverage tests."""
    return [{'account_number': '12345', 'name': 'John', 'status': 'A', 'balance': 100.0, 'plan': 'NP'}]

@pytest.fixture
def dummy_accounts():
    """Provides account for decision/loop coverage tests."""
    return [{'account_number': '12345', 'balance': 100.0, 'total_transactions': 0}]


# PART 1: Statement Coverage (write.py)

def test_tc1_1_valid_account(base_account, tmp_path):
    output_file = tmp_path / "test_output.txt"
    write_new_current_accounts(base_account, str(output_file))
    assert output_file.exists()

def test_tc1_2_non_numeric_acc(base_account, tmp_path):
    base_account[0]['account_number'] = '12A45'
    output_file = tmp_path / "test_output.txt"
    with pytest.raises(ValueError, match="Account number must be numeric"):
        write_new_current_accounts(base_account, str(output_file))

def test_tc1_3_acc_too_long(base_account, tmp_path):
    base_account[0]['account_number'] = '123456'
    output_file = tmp_path / "test_output.txt"
    with pytest.raises(ValueError, match="Account number exceeds 5 digits"):
        write_new_current_accounts(base_account, str(output_file))

def test_tc1_4_name_too_long(base_account, tmp_path):
    base_account[0]['name'] = 'ThisNameIsWayTooLongForTheProgram'
    output_file = tmp_path / "test_output.txt"
    with pytest.raises(ValueError, match="Account name exceeds 20"):
        write_new_current_accounts(base_account, str(output_file))

def test_tc1_5_invalid_status(base_account, tmp_path):
    base_account[0]['status'] = 'X'
    output_file = tmp_path / "test_output.txt"
    with pytest.raises(ValueError, match="Invalid status"):
        write_new_current_accounts(base_account, str(output_file))

def test_tc1_6_non_numeric_balance(base_account, tmp_path):
    base_account[0]['balance'] = 'OneHundred'
    output_file = tmp_path / "test_output.txt"
    with pytest.raises(ValueError, match="Balance must be numeric"):
        write_new_current_accounts(base_account, str(output_file))

def test_tc1_7_negative_balance(base_account, tmp_path):
    base_account[0]['balance'] = -50.0
    output_file = tmp_path / "test_output.txt"
    with pytest.raises(ValueError, match="Negative balance detected"):
        write_new_current_accounts(base_account, str(output_file))

def test_tc1_8_balance_exceeds_max(base_account, tmp_path):
    base_account[0]['balance'] = 100000.00
    output_file = tmp_path / "test_output.txt"
    with pytest.raises(ValueError, match="Balance exceeds maximum"):
        write_new_current_accounts(base_account, str(output_file))

def test_tc1_9_invalid_plan(base_account, tmp_path):
    base_account[0]['plan'] = 'XX'
    output_file = tmp_path / "test_output.txt"
    with pytest.raises(ValueError, match="Invalid plan type"):
        write_new_current_accounts(base_account, str(output_file))


# PART 2: Decision and Loop Coverage (main_backend.py)

def test_tc2_1_file_not_found(dummy_accounts):
    result = process_transactions(dummy_accounts, "does_not_exist.txt")
    assert result == dummy_accounts

def test_tc2_2_loop_zero_times(dummy_accounts, tmp_path):
    trans_file = tmp_path / "temp_trans.txt"
    trans_file.write_text("")  # Empty file means loop runs 0 times
    result = process_transactions(dummy_accounts, str(trans_file))
    assert result == dummy_accounts

def test_tc2_3_blank_line(dummy_accounts, tmp_path):
    trans_file = tmp_path / "temp_trans.txt"
    trans_file.write_text("   \n")
    result = process_transactions(dummy_accounts, str(trans_file))
    assert result[0]['balance'] == 100.0

def test_tc2_4_session_code(dummy_accounts, tmp_path):
    trans_file = tmp_path / "temp_trans.txt"
    trans_file.write_text("10 admin 00000 00000 **\n")
    result = process_transactions(dummy_accounts, str(trans_file))
    assert result[0]['balance'] == 100.0

def test_tc2_5_deposit_match(dummy_accounts, tmp_path):
    trans_file = tmp_path / "temp_trans.txt"
    trans_file.write_text("04 12345 50.00 00000 **\n")
    result = process_transactions(dummy_accounts, str(trans_file))
    assert result[0]['balance'] == 150.0

def test_tc2_6_deposit_no_match(dummy_accounts, tmp_path):
    trans_file = tmp_path / "temp_trans.txt"
    trans_file.write_text("04 99999 50.00 00000 **\n")  # Wrong account number
    result = process_transactions(dummy_accounts, str(trans_file))
    assert result[0]['balance'] == 100.0  # Balance should not change