#!/bin/bash

# Usage: ./test.sh [--with-coverage] [reports-directory]
# If reports directory is not specified, a default one is used.
# If --with-coverage is specified, coverage reports are generated.

# Initialize variables
WITH_COVERAGE=false
REPORTS_DIR="./reports" # Default reports directory

# Source common functions
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
source "$script_dir/../support/testing/functions.sh"

# Parse flags
while getopts ":h" option; do
    case $option in
        h) # display Help
            echo "Usage: $0 [--with-coverage] [reports-directory]"
            exit;;
        \?) # Invalid option
            echo "Error: Invalid option"
            exit;;
    esac
done

# Check remaining arguments after options are processed
shift "$((OPTIND-1))"

# Check if --with-coverage flag is present
for arg in "$@"; do
    if [[ $arg == "--with-coverage" ]]; then
        WITH_COVERAGE=true
        # Remove --with-coverage from arguments
        set -- "${@/--with-coverage/}"
        break
    fi
done

# Check if reports directory argument is provided
if [ "$#" -ge 1 ]; then
    REPORTS_DIR=$1
fi

SERVICE_NAME="ms-test-sample"


echo "Running tests for $SERVICE_NAME..."
build_docker_image "$SERVICE_NAME" "$script_dir"

if $WITH_COVERAGE; then
    echo "Running tests with coverage..."
    run_docker_container_python "$SERVICE_NAME" "$REPORTS_DIR"
    modify_coverage_report_python "$SERVICE_NAME" "$REPORTS_DIR"
else
    echo "Running tests without coverage..."
    # Assuming there's a function or a command to run tests without generating coverage reports
    run_docker_container_python_without_coverage "$SERVICE_NAME"
fi