#!/bin/bash

if [ ! -f ./.last_environment ]; then
    echo "No environment information found. Using dev as defail argument."
    ENVIRONMENT=dev
else
    ENVIRONMENT=$(cat ./.last_environment)
    
fi


stop_docker() {
    echo "Taking down the Docker Compose environment for $ENVIRONMENT..."
    docker compose -f docker-compose.base.yml -f docker-compose.$ENVIRONMENT.yml -f docker-compose.support.yml down
}

# Stop the environment
stop_docker