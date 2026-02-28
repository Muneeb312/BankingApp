#!/bin/sh

# Testing Script for Frontend
#
# Component Directory Map
# ./input/    - Test Inputs
# ./expected/ - Test Outputs (Expected)
# ./actual/   - Test Outputs (Actual)
#
# This script runs the frontend program with a set of predefined inputs, saves the program's outputs, then compares the outputs with expected predefined outputs.

APP_CMD="python main.py"
ACCOUNTS_FILE="valid_accounts.txt"
INPUT_DIR="./input"
EXPECTED_DIR="./expected"
ACTUAL_DIR="./actual"

echo "[i] Starting Test Procedure..."
# cd ./input/
rm -rf ./actual/*

TEST_COUNT=$(find . -type f -name "*.atf" | wc -l)
echo "[i] $TEST_COUNT tests to run..."

find "$INPUT_DIR" -type f -name "*.atf" | while read -r input_file; do

    # Remove './input/' from the beginning 
    rel_path="${input_file#$INPUT_DIR/}"
    #Extract just the folder name 
    sub_dir=$(dirname "$rel_path")
    
    # Extract just the filename without .atf
    base_name=$(basename "$rel_path" .atf)

    echo "[RUN] Testing: $sub_dir/$base_name"

    # create 'actual' folder
    mkdir -p "$ACTUAL_DIR/$sub_dir"

    # file paths
    actual_term="$ACTUAL_DIR/$sub_dir/${base_name}.out"
    actual_trans="$ACTUAL_DIR/$sub_dir/${base_name}.atf"
    expected_term="$EXPECTED_DIR/$sub_dir/${base_name}.out"
    expected_trans="$EXPECTED_DIR/$sub_dir/${base_name}.etf"

    $APP_CMD "$ACCOUNTS_FILE" "$actual_trans" < "$input_file" > "$actual_term"

    # validate output
    if diff -qw "$expected_term" "$actual_term" > /dev/null 2>&1; then
        echo "  ├── [PASS] Terminal Output"
    else
        echo "  ├── [FAIL] Terminal Output" 
    fi  

    # validate transaction file output
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

echo "[i] Testing Procedure Complete."