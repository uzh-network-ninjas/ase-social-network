#!/bin/bash

# Set default environment to dev
ENVIRONMENT="dev"
BUILD_FLAG=false
POWERSHELL=false

# Function to parse command line arguments
parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      dev|test)
        ENVIRONMENT=$1
        shift # move to next argument
        ;;
      -b)
        BUILD_FLAG=true
        shift # move past the argument
        ;;
      -p)
        POWERSHELL=true
        shift # move past the argument
        ;;
      *)
        echo "Unsupported environment or option: $1. Use 'dev' or 'test', with optional flags '-b' or '-p'."
        exit 1
        ;;
    esac
  done
}


# Function to start the Docker environment
start_docker() {
  # docker network create ms-net
  if $BUILD_FLAG; then
    echo "Building Docker images..."
    docker compose --env-file .env -f docker-compose.base.yml -f docker-compose.dev.yml -f docker-compose.support.yml build
  fi
  echo "Starting Docker containers in development environment..."
  docker compose --env-file .env -f docker-compose.base.yml -f docker-compose.dev.yml -f docker-compose.support.yml up -d
}

start_test() {
  # docker network create ms-net
  if $BUILD_FLAG; then
    echo "Building Docker images..."
    docker compose --env-file .env -f docker-compose.base.yml -f docker-compose.test.yml -f docker-compose.support.yml build
  fi
  echo "Starting Docker containers in test environment..."
  docker compose --env-file .env -f docker-compose.support.yml -f docker-compose.base.yml -f docker-compose.test.yml up -d
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
      exit 1
    fi
    ;;
  test)
    if [ -f ".env" ]; then
      start_test
    else
      echo "The .env file does not exist. Please create it before starting."
      exit 1
    fi
    ;;
  *)
    echo "Unsupported environment. Use 'dev' or 'test'."
    exit 1
    ;;
esac

echo $ENVIRONMENT > ./.last_environment

echo -e "\033[0;32mUse the application at http://localhost:8000\033[0m"

if $POWERSHELL; then
  echo "Press any key to continue..."
  read -n 1 -s -r
fi