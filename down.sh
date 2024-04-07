#!/bin/bash

# Function to stop Docker environment
stop_docker() {
  docker compose -f docker-compose.base.yml -f docker-compose.dev.yml -f docker-compose.kong.yml down
}

echo "Taking down the Docker Compose environment..."
stop_docker