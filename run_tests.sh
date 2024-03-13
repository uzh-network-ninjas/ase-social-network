#!/bin/bash

# Usage: ./run_tests.sh [--with-coverage] <microservice-name> or ./run_tests.sh [--with-coverage] '*' to run for all services

# Initialize variables
WITH_COVERAGE=false
REPORTS_DIR="./reports"

# Source the microservices from services.conf
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
source $script_dir/support/testable_services.conf

# Function to run tests for a single service
run_tests_for_service() {
    local service_name=$1
    echo "Running tests for $service_name"
    
    # Depending on the WITH_COVERAGE flag, pass the appropriate arguments
    if $WITH_COVERAGE; then
        ./"$service_name"/test.sh "${REPORTS_DIR}" --with-coverage
    else
        ./"$service_name"/test.sh
    fi
}

# Parse command-line options
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --with-coverage) WITH_COVERAGE=true; shift ;;
        -h|--help) echo "Usage: $0 [--with-coverage] <microservice-name> or $0 [--with-coverage] '*' to run for all services"; exit ;;
        *) break ;;
    esac
done

# After parsing options, check if a microservice name was provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 [--with-coverage] <microservice-name> or $0 [--with-coverage] '*' to run for all services"
    exit 1
fi

service_name="$1"

# Execute the tests based on the provided service name or wildcard
if [[ "$service_name" == "*" ]]; then
    for service in "${services[@]}"; do
        run_tests_for_service "$service"
    done
else
    # Check if the provided service name exists in the services array
    service_exists=false
    for service in "${services[@]}"; do
        if [[ "$service" == "$service_name" ]]; then
            service_exists=true
            break
        fi
    done
    
    if ! $service_exists; then
        echo "Error: Microservice '$service_name' does not exist."
        exit 1
    fi
    
    run_tests_for_service "$service_name"
fi
