#!/bin/bash

# Define the most important part, the service name
SERVICE_NAME="ms-review"

# Import common functions and variables
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
source "$script_dir/../support/testing/setup_test_file.sh"

# import functions (definition of seting up container, executing scrpt for python etc)
source "$script_dir/../support/testing/functions.sh"

# Parse command-line arguments
parse_args "$@"

# Now, $WITH_COVERAGE and $REPORTS_DIR are set by common_setup.sh

echo "Running tests for $SERVICE_NAME..."
build_docker_image "$SERVICE_NAME" "$script_dir"

if $WITH_COVERAGE; then
    echo "Running tests with coverage..."
    run_docker_container_python "$SERVICE_NAME" "$REPORTS_DIR"
    modify_coverage_report_python "$SERVICE_NAME" "$REPORTS_DIR"
else
    echo "Running tests without coverage..."
    run_docker_container_python_without_coverage "$SERVICE_NAME"
fi