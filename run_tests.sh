#!/bin/sh

# Testing Script for Frontend
#
# Component Directory Map
# ./input/    - Test Inputs
# ./expected/ - Test Outputs (Expected)
# ./actual/   - Test Outputs (Actual)
#
# This script runs the frontend program with a set of predefined inputs, saves the program's outputs, then compares the outputs with expected predefined outputs.

echo "[i] Starting Test Procedure..."
cd ./input/
TEST_COUNT=$(find . -type f -name "*.atf" | wc -l)
echo "[i] $TEST_COUNT tests to run..."

