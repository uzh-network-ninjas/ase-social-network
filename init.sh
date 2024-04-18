#!/bin/bash

# Set default environment to dev
ENVIRONMENT="dev"
BUILD_FLAG=false

# Function to parse command line arguments
parse_args() {
  while getopts ":b" opt; do
    case $opt in
      b)
        BUILD_FLAG=true
        ;;
      \?)
        echo "Invalid option: -$OPTARG" >&2
        exit 1
        ;;
      :)
        echo "Option -$OPTARG requires an argument." >&2
        exit 1
        ;;
    esac
  done

  # Shift off the options and optional --
  shift $((OPTIND-1))

  # Remaining argument is the environment, if any
  if [ $# -gt 0 ]; then
    ENVIRONMENT=$1
  fi
}

# Function to start the Docker environment
start_docker() {
  if $BUILD_FLAG; then
    echo "Building Docker images..."
    docker compose --env-file .env -f docker-compose.base.yml -f docker-compose.dev.yml -f docker-compose.kong.yml build
  fi
  echo "Starting Docker containers in development environment..."
  docker compose --env-file .env -f docker-compose.base.yml -f docker-compose.dev.yml -f docker-compose.kong.yml up -d
}

start_test() {
  if $BUILD_FLAG; then
    echo "Building Docker images..."
    docker compose --env-file .env -f docker-compose.base.yml -f docker-compose.test.yml -f docker-compose.kong.yml build
  fi
  echo "Starting Docker containers in test environment..."
  docker compose --env-file .env -f docker-compose.base.yml -f docker-compose.test.yml -f docker-compose.kong.yml up -d
}

# Parse command line arguments
parse_args "$@"

# Start based on the environment
case $ENVIRONMENT in
  dev)
    if [ -f ".env" ]; then
      start_docker
    else
      echo "The .env file does not exist. Please create it before starting."
    fi
    ;;
  test)
    if [ -f ".env" ]; then
      start_test
    else
      echo "The .env file does not exist. Please create it before starting."
    fi
    ;;
  *)
    echo "Unsupported environment. Use 'dev' or 'test'."
    ;;
esac

echo $ENVIRONMENT > ./.last_environment