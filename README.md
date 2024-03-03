## Setup
- You need to have docker installed with docker-compose
- simply run `.start-service.sh` to setup everything

## what it does
- it will create a docker network
- it will launch `docker-compose.yml` file, with all microservices
- it will launch `docker-compose.kong.yml` file, with kong gateway

# How to create new microservice?
- create new folder in the main repo
- create `Dockerfile` in newly created repo
- add the service to `docker-compose.yml` file with all dependencies, lie DB etc
- add the service to `/kong/initialize-kong.sh` file, to register the service automatically into kong

## current Setup
- Python development can be done freely in folder, because it runs with volume connected and --refresh flag
- Kongo must be added manually or just whole setup must be done
