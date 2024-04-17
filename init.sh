#!/bin/bash

# Set default environment to dev
ENVIRONMENT="dev"

# Check if an argument was provided
if [ $# -gt 0 ]; then
  ENVIRONMENT=$1
fi

# Function to start the Docker environment
start_docker() {
  docker compose --env-file .env -f docker-compose.base.yml -f docker-compose.dev.yml -f docker-compose.kong.yml up -d
}

start_test(){
  docker compose --env-file .env -f docker-compose.base.yml -f docker-compose.test.yml -f docker-compose.kong.yml up -d
}

# Start based on the environment
case $ENVIRONMENT in
  dev)
    if [ -f ".env" ]; then
      echo "Starting in development environment..."
      start_docker
    else
      echo "The .env file does not exist. Please create it before starting."
    fi
    ;;
  test)
    if [ -f ".env" ]; then
      echo "Starting in test environment..."
      start_test
    else
      echo "The .env file does not exist. Please create it before starting."
    fi
    ;;
  *)
    echo "Unsupported environment. Use 'dev' or 'test'."
    ;;
esac