## Setup
- You need to have docker installed with docker-compose
- simply run `.init.sh` to setup everything (works in Cygwin for example)
- otherwise run and `docker-compose -f docker-compose.yml -f docker-compose.kong.yml up` to start local development
- each microservice should have 'swagger' available under `/docs` endpoint (one must access direct the endpoint of each microservice)
- Kongo admin available at `http://localhost:8002/`

## what does `.init.sh` do?
- it will create a docker network
- it will launch `docker-compose.yml` file, with all microservices
- it will launch `docker-compose.kong.yml` file, with kong gateway

# How to create new microservice?
- create new folder in the main repo
- create `Dockerfile` in newly created repo
- add the service to `docker-compose.yml` file with all dependencies, like DB etc
- add the service to the `kong/config/kong.yml` file (name and routes needed)

## current Setup
- Python development can be done freely in folder, because it runs with volume connected and --refresh flag
- Kongo must be added manually or just whole setup must be done


## TODO 
- create development docker compose
- create a function that extracts user UUID from a token - and reuse this function in all microservices


## User registration flow
- Register as a user with password
- then Issue a token via /token - Accepts username and password in FormData (can be changed)
- this issues a JSON Web Token (JWT) that can be used to authenticate requests to the protected endpoints


