#!/bin/bash
# weekly.sh
# Usage: ./weekly.sh

STARTING_MASTER="master_day0.txt"
SESSIONS_BASE_DIR="sessions"

echo "=== Starting Weekly Batch Process Simulation ==="

# Ensure the Day 0 master file exists before attempting to run the week
if [ ! -f "$STARTING_MASTER" ]; then
    echo "Error: Starting master file '$STARTING_MASTER' not found in root directory!"
    exit 1
fi

# Loop to simulate 7 consecutive days
for day in {1..7}; do
    input_sessions="$SESSIONS_BASE_DIR/day$day"
    current_master="master_day$((day-1)).txt"
    new_master="master_day$day.txt"

    echo ""
    echo "==========================================="
    echo " Executing Day $day"
    echo "==========================================="

    # Execute the daily script with the dynamically generated file paths
    ./daily.sh "$input_sessions" "$current_master" "$new_master"

    # Catch potential errors to prevent compounding bad data
    if [ $? -ne 0 ]; then
        echo "Error: Daily processing failed on Day $day. Halting weekly run."
        exit 1
    fi
done

echo ""
echo "=== Weekly Batch Process Complete ==="
echo "Final master accounts file generated: master_day7.txt"