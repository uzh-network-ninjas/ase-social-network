#!/bin/bash

# Wait for Kong to be ready
echo "Waiting for Kong to be ready..."
while ! curl -s http://localhost:8001/ > /dev/null; do
  sleep 1
done
echo "Kong is up and running!"

# Configure services and routes
# ms-user service
curl -i -X POST --url http://localhost:8001/services/ --data 'name=ms-user-service' --data 'url=http://ms-user:5000'
curl -i -X POST --url http://localhost:8001/services/ms-user-service/routes --data 'paths[]=/users'

# ms-post service
curl -i -X POST --url http://localhost:8001/services/ --data 'name=ms-post-service' --data 'url=http://ms-post:5001'
curl -i -X POST --url http://localhost:8001/services/ms-post-service/routes --data 'paths[]=/posts'


echo "Services and routes configured!"