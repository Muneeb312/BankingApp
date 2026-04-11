#!/bin/bash
# daily.sh
# Usage: ./daily.sh <session_directory> <current_master_file> <new_master_file>

SESSION_DIR=$1
CURRENT_MASTER=$2
NEW_MASTER=$3

MERGED_TRANS="merged_daily_transactions.txt"
VALID_ACCOUNTS="valid_accounts.txt"
FRONTEND_CMD="py main.py"
BACKEND_CMD="py main_backend.py"

echo "--- Starting Daily Processing for $SESSION_DIR ---"

# Clear out the merged transaction file from the previous day
> "$MERGED_TRANS"
# Loops through every .txt file inside the day's session folder
for session_file in "$SESSION_DIR"/*.txt; do
    if [ -f "$session_file" ]; then
        session_name=$(basename "$session_file" .txt)
        temp_trans="${session_name}_trans.atf"

        echo "[*] Processing Front End session: $session_name"
        # Feed the session text file into the Front End
        # Note: Adjust the arguments here if your group member's Front End requires different parameters
        $FRONTEND_CMD "$VALID_ACCOUNTS" "$temp_trans" < "$session_file"

        # Concatenate the output into the merged file
        cat "$temp_trans" >> "$MERGED_TRANS"

        # Clean up the temporary individual transaction file
        rm "$temp_trans"
    fi
done

# Run the back end
echo "[*] Running Back End with Merged Transactions..."
$BACKEND_CMD "$CURRENT_MASTER" "$MERGED_TRANS" "$NEW_MASTER"

echo "--- Daily Processing Complete. Output generated: $NEW_MASTER ---"

py -c "
import sys
filename = sys.argv[1]
with open(filename, 'r') as f:
    lines = f.readlines()
with open(filename, 'w') as f:
    for line in lines:
        line = line.rstrip() # Remove the newline
        if len(line) > 2:
            # Take everything except the last 2 chars, add '0000 ', then add the last 2 chars
            fixed_line = line[:-2] + '0000 ' + line[-2:] + '\n'
            f.write(fixed_line)
" "$NEW_MASTER"

