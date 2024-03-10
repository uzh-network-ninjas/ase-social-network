#!/bin/bash

# Usage: ./run_tests_and_upload_coverage.sh service1 service2 or ./run_tests_and_upload_coverage.sh '*' to run for all services

# Configuration settings
REPORTS_DIR="./reports"
CODECOV_TOKEN="<your_codecov_token_here>" # You should ideally pass this as an environment variable
GITHUB_RUN_ID="${GITHUB_RUN_ID:-$(date +%s)}" # Use current timestamp as fallback if GITHUB_RUN_ID is not set

# Define all services
all_services=("ms-test-sample" "another-service" "yet-another-service") # Add all your service names here

# if input is * then services = all services
if [ "$1" == "*" ]; then
    services=("${all_services[@]}")
else
    services=("$@")
fi

# Ensure the reports directory exists
mkdir -p "${REPORTS_DIR}"

# Iterate over all provided service names
for service in "${services[@]}"; do
    echo "Processing $service..."

    # Run tests for the service (your existing test logic here)
    # Assuming your tests generate coverage-service.xml in the current directory
    bash ./run_tests.sh "$service"

    # Check if the coverage report exists, then upload it
    if [ -f "${REPORTS_DIR}/coverage_${service}.xml" ]; then
        ./codecov --verbose upload-process --fail-on-error -t "${CODECOV_TOKEN}" -n "${service}-${GITHUB_RUN_ID}" -F "$service" -f "${REPORTS_DIR}/coverage_${service}.xml"
    else
        echo "No coverage report found for $service."
    fi