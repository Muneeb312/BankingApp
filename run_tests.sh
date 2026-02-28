#!/bin/sh

# BankingApp Testing Script
#
# Component Directory Map
# ./tests/input/           - Test Inputs
# ./tests/output/expected/ - Test Outputs (Expected)
# ./tests/output/actual/   - Test Outputs (Actual)
#
# This script runs the BankingApp frontend program with a set of predefined inputs, saves the program's outputs, then compares the outputs with expected predefined outputs.

# Program Testing Variables
APP_CMD="python3 main.py" # Main Executable Command
ACCOUNTS_FILE="valid_accounts.txt" # Accounts File
INPUT_DIR="./tests/input" # Program Inputs
EXPECTED_DIR="./tests/output/expected" # Expected Program Outputs
ACTUAL_DIR="./tests/output/actual" # Actual Program Outputs

# Start Testing
echo "[i] Starting Test Procedure..."
# Clean up previously generated test outputs.
if [ -d "$ACTUAL_DIR" ]; then
    rm -r $ACTUAL_DIR
fi
# Count number of tests to run.
TEST_COUNT=$(find . -type f -name "*.atf" | wc -l)
echo "[i] $TEST_COUNT tests to run..."

# Testing Loop
find "$INPUT_DIR" -type f -name "*.atf" | while read -r input_file; do
    # Get relative path of input file.
    rel_path="${input_file#$INPUT_DIR/}"
    # Get folder name.
    sub_dir=$(dirname "$rel_path")
    # Get file name without extension.
    base_name=$(basename "$rel_path" .atf)

    # Run Test
    echo "[RUN] Testing: $sub_dir/$base_name"

    # Create Test Output folder.
    mkdir -p "$ACTUAL_DIR/$sub_dir"

    # File Paths
    actual_term="$ACTUAL_DIR/$sub_dir/${base_name}.out" # Terminal Output
    actual_trans="$ACTUAL_DIR/$sub_dir/${base_name}.atf" # Transaction File Output
    expected_term="$EXPECTED_DIR/$sub_dir/${base_name}.out" # Expected Terminal Output
    expected_trans="$EXPECTED_DIR/$sub_dir/${base_name}.etf" # Expected Transaction File Output

    # Execute program with test parameters.
    $APP_CMD "$ACCOUNTS_FILE" "$actual_trans" < "$input_file" > "$actual_term"

    # Validate Terminal Output against Expected Terminal Output.
    if diff -qw "$expected_term" "$actual_term" > /dev/null 2>&1; then
        echo "  ├── [PASS] Terminal Output"
    else
        echo "  ├── [FAIL] Terminal Output" 
    fi  
    # Validate Transaction File Output against Expected Transaction File Output.
    if [ -f "$expected_trans" ]; then
        if diff -qw "$expected_trans" "$actual_trans" > /dev/null 2>&1; then
            echo "  └── [PASS] Transaction File"
        else
            echo "  └── [FAIL] Transaction File"
        fi
    else
        echo "  └── [INFO] No expected transaction file provided."
    fi
done

# End
echo "[i] Testing Procedure Complete."
