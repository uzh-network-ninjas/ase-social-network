#!/bin/bash

# Start main services in detached mode
echo "Starting main services..."
docker compose -f docker-compose.yml up --build -d

# Start Kong services in detached mode
echo "Starting Kong services..."
docker compose -f docker-compose.kong.yml up -d #TODO cannot be runned with --build determine why??

# Check if Kong is up by making a request to the admin API
echo "Waiting for Kong to be ready..."
until $(curl --output /dev/null --silent --head --fail http://localhost:8001); do
    printf '.'
    sleep 5
done
echo "Kong is up and running."

# Execute Kong configuration script
echo "Configuring Kong..."
./kong/initialize-kong.sh

echo "Services and Kong configuration completed."