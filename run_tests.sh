#!/bin/bash

# Usage: ./run_tests.sh [--with-coverage] [--unit-tests <microservice-name> | --unit-tests '*'] [--e2e-tests]
# Default behavior runs both unit and e2e tests for all services without coverage if no flags are provided.

# Initialize variables
WITH_COVERAGE=false
RUN_UNIT_TESTS=false
RUN_E2E_TESTS=false

UNIT_TEST_SERVICE_SPECIFIED=false
UNIT_TEST_SERVICES=() # This will be populated based on the --unit-tests option

# Source the microservices from services.conf
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
echo $script_dir
source "$script_dir/support/testable_services.conf"
REPORTS_DIR=$script_dir"/reports"

# Function to run unit tests for a single service
run_unit_tests_for_service() {
    local service_name=$1
    echo "Running unit tests for $service_name"
    
    if $WITH_COVERAGE; then
        "$script_dir"/"$service_name"/test.sh "${REPORTS_DIR}" --with-coverage
    else
        "$script_dir"/"$service_name"/test.sh
    fi
}

# Function to run e2e tests
run_e2e_tests() {
    echo "Running e2e tests"
    # Start all services with Docker Compose
    echo "Starting all services..."

    # copy .env.example to .env
    cp .env.example .env
    # execute this -> from the main script
    $script_dir/init.sh test -b
    if $WITH_COVERAGE; then
        echo "running e2e tests with coverage"
        $script_dir/support/testing/run_e2e_tests.sh "${REPORTS_DIR}" --with-coverage
    else
        $script_dir/support/testing/run_e2e_tests.sh
    fi

    echo "taking down infrastructure"
    $script_dir/down.sh
}

# Parse command-line options
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --with-coverage)
            WITH_COVERAGE=true
            shift
            ;;
        --unit-tests)
            RUN_UNIT_TESTS=true
            UNIT_TEST_SERVICE_SPECIFIED=true
            if [[ "$2" != "--"* ]]; then # Ensure the next argument is not another flag
                UNIT_TEST_SERVICES+=("$2")
                shift # Move past the service name argument
            fi
            shift
            ;;
        --e2e-tests)
            RUN_E2E_TESTS=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--with-coverage] [--unit-tests <microservice-name> | --unit-tests '*'] [--e2e-tests]"
            exit 0
            ;;
        *) # Unknown option
            echo "Error: Unknown option $1"
            exit 1
            ;;
    esac
done

# Default to running both unit and e2e tests if neither option is specified
if ! $UNIT_TEST_SERVICE_SPECIFIED && ! $RUN_E2E_TESTS; then
    RUN_UNIT_TESTS=true
    RUN_E2E_TESTS=true
    UNIT_TEST_SERVICES=("${services[@]}") # Default to all services if none specified
fi

# Execute unit tests if specified
if $RUN_UNIT_TESTS; then
    if [ ${#UNIT_TEST_SERVICES[@]} -eq 0 ] || [[ "${UNIT_TEST_SERVICES[0]}" == "*" ]]; then
        # Run for all services if '*' is provided or no specific service is specified
        for service in "${services[@]}"; do
            run_unit_tests_for_service "$service"
        done
    else
        # Run for each specified service
        for service_name in "${UNIT_TEST_SERVICES[@]}"; do
            run_unit_tests_for_service "$service_name"
        done
    fi
fi

# Execute e2e tests if specified
if $RUN_E2E_TESTS; then
    run_e2e_tests
fi
