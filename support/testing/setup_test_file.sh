#!/bin/bash

# Default values
WITH_COVERAGE=false
REPORTS_DIR="./reports"
# SERVICE_NAME=not-identified" # cannot be defined there -> ottherwise conflict with main scripts

# Parse command-line arguments
function parse_args() {
    while getopts ":h" option; do
        case $option in
            h) # Display Help
                echo "Usage: $0 [--with-coverage] [reports-directory]"
                exit;;
            \?) # Invalid option
                echo "Error: Invalid option"
                exit;;
        esac
    done

    # Check remaining arguments after options are processed
    shift "$((OPTIND-1))"

    # Check for --with-coverage flag
    for arg in "$@"; do
        if [[ $arg == "--with-coverage" ]]; then
            WITH_COVERAGE=true
            # Remove --with-coverage from arguments
            set -- "${@/--with-coverage/}"
            break
        fi
    done

    # Check if reports directory argument is provided
    if [ "$#" -ge 1 ]; then
        REPORTS_DIR=$1
    fi
}