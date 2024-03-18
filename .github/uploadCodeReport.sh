#!/bin/bash

# Usage: ./run_tests_and_upload_coverage.sh service1 service2 or ./run_tests_and_upload_coverage.sh '*' to run for all services

# if input is * then services = all services
if [ "$1" == "*" ]; then
    services=("ms-test-sample")
else
    services=("$@")
fi

# Iterate over all provided service names
for service in services; do
    echo "Processing $service..."

    # Run tests for the service (your existing test logic here)
    # Assuming your tests generate coverage-service.xml in the current directory
    bash ./run_tests.sh "$service"

    # Check if the coverage report exists, then upload it
    if [ -f "./reports/coverage_${service}.xml" ]; then
        ./codecov --verbose upload-process --fail-on-error -t "${CODECOV_TOKEN}" -n "${service}-${GITHUB_RUN_ID}" -F "$service" -f "./reports/coverage_${service}.xml"
    else
        echo "No coverage report found for $service."
    fi
done