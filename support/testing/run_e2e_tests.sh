#!/bin/bash

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# Import if with coverage and reports dir
source "$script_dir/setup_test_file.sh"

# parse arguments via setup functions
parse_args "$@"

cypress_dir=$script_dir"/e2etesting"
target_machine_dir="app"

if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
      volume_path="${cypress_dir}:/${target_machine_dir}"
  elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "win32"* ]]; then
      # Attempt to generate a Windows-style path (e.g., C:\path\to\reports)
      win_path=$(cd "$cypress_dir" && pwd -W 2>/dev/null)
      if [ -n "$win_path" ]; then
          volume_path="${win_path}:/${target_machine_dir}"
      else
          # Fallback to the current approach but simplified without unnecessary echo/sed
          volume_path="$(pwd -W)/${cypress_dir}:/${target_machine_dir}"
          volume_path="${volume_path//\//\\}"  # Convert all forward slashes to backslashes
          volume_path="${volume_path/C:\\/C:/}" # Simplify leading drive letter path
      fi
  else
      volume_path="/${reports_dir}:/${target_machine_dir}"
  fi

  echo "volume path: ${volume_path}"
  
if $WITH_COVERAGE; then
  
    REPORT_FILE="${REPORTS_DIR}/e2e_test_results.txt"
    GITHUB_REPORT_FILE="${REPORTS_DIR}/e2e_test_results.md"
    mkdir -p "${REPORTS_DIR}"

    echo "Running tests with coverage..."

    # uncomment for debugging 
    # docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'

    # # curl verbose output to localhost:8000
    total_calls=1

    # # URL to request
    url="http://localhost:8000"

    # Loop for a total of 10 calls
    for ((i=1; i<=total_calls; i++))
    do
    echo "Making call $i to $url"
    # Use curl with the -v option for verbose output
    curl -v -I  $url
    
    # Check if it is not the last iteration to avoid an unnecessary sleep
    if [ $i -lt $total_calls ]; then
        echo "Sleeping for 10 seconds..."
        sleep 10
    fi
    done

    # Uncomment for debugging
    # netstat -lt

    # get proper name by grep "kong"
    

    MSYS_NO_PATHCONV=1 docker run --network host -v $volume_path -w "/app" \
    cypress/included:latest \
    --config baseUrl=http://localhost:8000  \
    --reporter-options "toConsole=true" | tee $REPORT_FILE

    if [ -s $REPORT_FILE ]; then
        # Print everything after "Run Finished"
        $script_dir/convert_cypress_to_MD.sh $REPORT_FILE $GITHUB_REPORT_FILE
    else
        echo "No output found or file is empty."
    fi

    # find out if $GITHUB_REPORT_FILE has string x of x failed 
    if grep -q -e "failed" -e "No relevant test result summary found" $GITHUB_REPORT_FILE; then
        echo "Tests failed please check the CI pipeline for more details"
        exit 1
    else
        echo "Tests passed"
    fi

else
    echo "Running tests without coverage..."
    MSYS_NO_PATHCONV=1 docker run --network host -v $volume_path  -w "/app" \
    cypress/included:latest   \
    --config baseUrl=http://localhost:8000 
fi

