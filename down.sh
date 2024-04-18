#!/bin/bash

if [ ! -f /last_environment.txt ]; then
    echo "No environment information found. Using dev as defail argument."
    ENVIRONMENT=dev
fi
else
    ENVIRONMENT=$(cat ./last_environment.txt)
    
fi


stop_docker() {
    echo "Taking down the Docker Compose environment for $ENVIRONMENT..."
    docker compose -f docker-compose.base.yml -f docker-compose.$ENVIRONMENT.yml -f docker-compose.kong.yml down
}

# Stop the environment
stop_docker