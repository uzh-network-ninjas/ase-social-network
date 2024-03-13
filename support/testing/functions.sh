#!/bin/bash

# Function to build the Docker image for a service
build_docker_image() {
    local service_name=$1
    local service_dir=$2
    docker build -t "${service_name}_test" "$service_dir"
}

# Function to determine the correct volume path format based on the OS and run Docker container
run_docker_container_python() {
    local service_name=$1
    local reports_dir=$2
    local volume_path=""

    if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
        volume_path="$(pwd)/${reports_dir}:/reports"
    elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "win32"* ]]; then
        # Attempt to generate a Windows-style path (e.g., C:\path\to\reports)
        win_path=$(cd "$reports_dir" && pwd -W 2>/dev/null)
        if [ -n "$win_path" ]; then
            volume_path="${win_path}:/reports"
        else
            # Fallback to the current approach but simplified without unnecessary echo/sed
            volume_path="$(pwd -W)/${reports_dir}:/reports"
            volume_path="${volume_path//\//\\}"  # Convert all forward slashes to backslashes
            volume_path="${volume_path/C:\\/C:/}" # Simplify leading drive letter path
        fi
    else
        volume_path="$(pwd)/${reports_dir}:/reports"
    fi

    # Ensure the reports directory exists
    mkdir -p "${reports_dir}"

    # Run Docker container
    docker run --rm -v "${volume_path}" "${service_name}_test" pytest --cov="app" --cov-report=xml:/reports/coverage_"${service_name}".xml
}

# Function to modify the coverage report
modify_coverage_report_python() {
    local service_name=$1
    local reports_dir=$2
    local coverage_report="${reports_dir}/coverage_${service_name}.xml"

    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/\/code\/app/\/${service_name}\/app/g" "$coverage_report"
    else
        sed -i "s/\/code\/app/\/${service_name}\/app/g" "$coverage_report"
    fi
}

run_docker_container_python_without_coverage() {
    local service_name=$1

    # Run Docker container
    docker run --rm "${service_name}_test" pytest
}