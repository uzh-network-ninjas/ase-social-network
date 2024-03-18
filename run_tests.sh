#!/bin/bash

# Usage: ./run_tests.sh [--with-coverage] [--unit-tests <microservice-name> | --unit-tests '*'] [--integration-tests]
# Default behavior runs both unit and integration tests for all services without coverage if no flags are provided.

# Initialize variables
WITH_COVERAGE=false
RUN_UNIT_TESTS=false
RUN_INTEGRATION_TESTS=false

UNIT_TEST_SERVICE_SPECIFIED=false
UNIT_TEST_SERVICES=() # This will be populated based on the --unit-tests option

# Source the microservices from services.conf
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
source "$script_dir/support/testable_services.conf"
REPORTS_DIR=$script_dir"/reports"

# Function to run unit tests for a single service
run_unit_tests_for_service() {
    local service_name=$1
    echo "Running unit tests for $service_name"

    # echo execution rights to test.sh
    ls -l $script_dir/"$service_name"/test.sh
    
    if $WITH_COVERAGE; then
        $script_dir/"$service_name"/test.sh "${REPORTS_DIR}" --with-coverage
    else
        $script_dir/"$service_name"/test.sh
    fi
}

# Function to run integration tests
run_integration_tests() {
    echo "Running integration tests"
    if $WITH_COVERAGE; then
        echo "No tests implemented yet --with-coverage"
    else
        echo "No tests implemented yet"
    fi
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
        --integration-tests)
            RUN_INTEGRATION_TESTS=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--with-coverage] [--unit-tests <microservice-name> | --unit-tests '*'] [--integration-tests]"
            exit 0
            ;;
        *) # Unknown option
            echo "Error: Unknown option $1"
            exit 1
            ;;
    esac
done

# Default to running both unit and integration tests if neither option is specified
if ! $UNIT_TEST_SERVICE_SPECIFIED && ! $RUN_INTEGRATION_TESTS; then
    RUN_UNIT_TESTS=true
    RUN_INTEGRATION_TESTS=true
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

# Execute integration tests if specified
if $RUN_INTEGRATION_TESTS; then
    run_integration_tests
fi
