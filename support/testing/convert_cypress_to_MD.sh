#!/bin/bash

# This script takes an input file and an output file as arguments.
input_file=$1
output_file=$2

# Check if the input file is provided and exists
if [[ -z "$input_file" || ! -f "$input_file" ]]; then
    echo "Input file is missing or does not exist."
    exit 1
fi

# Check if output file argument is provided
if [[ -z "$output_file" ]]; then
    echo "Output file name is required."
    exit 1
fi

# Read the last 10 lines of the input file
tail -n 10 "$input_file" > temp_last_10_lines.txt

# Search for "All specs passed!" in the last 10 lines
if grep -q "All specs passed!" temp_last_10_lines.txt; then
    echo "All specs passed!" > "$output_file"
else
    # If not found, search for the pattern "x of x failed"
    failure_message=$(grep -o "[0-9]\+ of [0-9]\+ failed" temp_last_10_lines.txt)
    if [[ -n "$failure_message" ]]; then
        echo "$failure_message" > "$output_file"
    else
        echo "No relevant test result summary found." > "$output_file"
    fi
fi

# Clean up temporary file
rm temp_last_10_lines.txt

echo "Results converted and saved to $output_file"