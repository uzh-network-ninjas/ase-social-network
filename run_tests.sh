#!/bin/bash

# Configuration settings
REPORTS_DIR="./reports"

# Array of service directories
services=("ms-test-sample")

# Loop through each service
for service in "${services[@]}"; do
    echo "Running tests for $service"
    
    # Build the Docker image for the service
    docker build -t "${service}_test" ./"$service"
    
    # Determine the correct volume path format based on the OS
    if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
        # Linux, Unix or macOS
        volume_path="$(pwd)/${REPORTS_DIR}:/reports"
    elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "win32"* ]]; then
        # Windows or using Git Bash/MINGW64
        # Attempt to use pwd -W to get a Windows-compatible path
        win_path=$(cd "$REPORTS_DIR" && pwd -W 2>/dev/null)
        if [ -n "$win_path" ]; then
            volume_path="${win_path}:/reports"
        else
            # Fallback if 'pwd -W' didn't work
            volume_path="$(pwd)/${REPORTS_DIR}:/reports"
            volume_path="$(echo $volume_path | sed 's/\/c\//c:\//; s/\//\\/g')"
        fi
    else
        # Unknown OS, fallback to default Unix-like behavior
        volume_path="$(pwd)/${REPORTS_DIR}:/reports"
    fi

    # Ensure the reports directory exists
    mkdir -p "${REPORTS_DIR}"

    # Run tests inside a Docker container and generate coverage report
    docker run --rm -v "${volume_path}" "${service}_test" pytest --cov="app" --cov-report=xml:/reports/coverage_"${service}".xml

done
