#!/bin/bash

# Usage: ./run_tests_and_upload_coverage.sh service1 service2 or ./run_tests_and_upload_coverage.sh '*' to run for all services

# Configuration settings
REPORTS_DIR="./reports"

# Define all services
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
source $script_dir/../support/testable_services.conf

# if input is * then services = all services
if [ "$1" == "*" ]; then
    services=("${all_services[@]}")
else
    services=("$@")
fi

echo "running" 
# Ensure the reports directory exists
mkdir -p "${REPORTS_DIR}"

# Iterate over all provided service names
for service in "${services[@]}"; do
    echo "Processing $service..."

    # Run tests for the service (always run with coverage because we want to upload the coverage report)
    # bash $script_dir/../run_tests.sh --with-coverage "$service" 

    # # Check if the coverage report exists, then upload it
    # if [ -f "${REPORTS_DIR}/coverage_${service}.xml" ]; then

    #     # Use the CODECOV_TOKEN and GITHUB_RUN_ID environment variables directly
    #     codecov -t "${CODECOV_TOKEN}" -n "${service}-${GITHUB_RUN_ID}" -F "$service" -f "${REPORTS_DIR}/coverage_${service}.xml"
    # else
    #     echo "No coverage report found for $service."
    # fi
done



# Workflow theoretical
# - Determine which services were changed - for tese run unittests
    # - If they do, upload the coverage report
# - Run overall integration tests (do they have coverage?)
