#!/bin/bash

# Usage: ./run_tests.sh <microservice-name> or ./run_tests.sh '*' to run for all services


# Configuration settings
REPORTS_DIR="./reports"

# Array of service directories
services=("ms-test-sample")

# Function to run tests for a single service
run_tests_for_service() {
    local service_name=$1
    echo "Running tests for $service_name"
    
    # Build the Docker image for the service
    docker build -t "${service_name}_test" ./"$service_name"
    
    # Determine the correct volume path format based on the OS
    local volume_path
    if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
        volume_path="$(pwd)/${REPORTS_DIR}:/reports"
    elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "win32"* ]]; then
        local win_path=$(cd "$REPORTS_DIR" && pwd -W 2>/dev/null)
        if [ -n "$win_path" ]; then
            volume_path="${win_path}:/reports"
        else
            volume_path="$(pwd)/${REPORTS_DIR}:/reports"
            volume_path="$(echo $volume_path | sed 's/\/c\//c:\//; s/\//\\/g')"
        fi
    else
        volume_path="$(pwd)/${REPORTS_DIR}:/reports"
    fi
    
    # Ensure the reports directory exists
    mkdir -p "${REPORTS_DIR}"
    
    # Run tests inside a Docker container and generate coverage report
    docker run --rm -v "${volume_path}" "${service_name}_test" pytest --cov="app" --cov-report=xml:/reports/coverage_"${service_name}".xml
}

# Check if a microservice name was provided as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <microservice-name> or $0 '*' to run for all services"
    exit 1
fi

service_name="$1"

# Check if the argument is the special asterisk for all services
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
    
    # Run tests for the specified service
    run_tests_for_service "$service_name"
fi
