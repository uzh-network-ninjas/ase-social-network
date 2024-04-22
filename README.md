## Setup
- You need to have docker installed with docker-compose
- simply run `./init.sh` to setup everything (works in Cygwin for example)
- otherwise run and `docker compose -f docker-compose.base.yml -f docker-compose.dev.yml -f docker-compose.kong.yml up` to start local development
- each microservice should have 'swagger' available under `/docs` endpoint (one must access direct the endpoint of each microservice)
- Kongo admin available at `http://localhost:8002/`
- turn off the infrastrucure `./down.sh`

## what does `./init.sh` do?
- it will create a docker network
- it will launch `docker-compose.base.yml` file, with all microservices and database structure
- it will launch `docker-compose.kong.yml` file, with kong gateway
- it will launch `docker-compose.dev.yml` file with exposure of the development ports

- You have option to add flag `-b`
  - this will trigger additional build of all docker compose files (useful mainly when adding new pip dependencies) 

# How to create new microservice?
- create new folder in the main repo
- create `Dockerfile` in newly created repo
- add the service to `docker-compose.yml` file with all dependencies, like DB etc
- add the service to the `kong/config/kong.yml` file (name and routes needed)

## current Setup
- Python development can be done freely in folder, because it runs with volume connected and --refresh flag
- Kongo must be added manually or just whole setup must be done

## User registration flow
- Register as a user with password via 
- then Issue a token via /token - Accepts username and password in FormData (can be changed) - (`http://localhost:8000/authenticator/token`)
- this issues a JSON Web Token (JWT) that can be used to authenticate requests to the protected endpoints


## helpful information during development
- if you add pip packages, you must build container with `--no-cache` flag, because otherwise will not install new packages
- if you change kong settings in kong.yml, you must SSH into kong container and run `kong reload` to apply changes
