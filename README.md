# Microservice-Powered Architecture Overview

This project implements a microservice-powered architecture
 utilizing Python microservices
 a Vue.js frontend
 and Kong as the API gateway. It includes support for local testing through Localstack
 and uses Grafana and Loki for logging capabilities. Below you'll find setup instructions
 development notes
 and testing guidelines to help you get started and manage the development process effectively.

## [Wiki for detailed information](https://github.com/uzh-network-ninjas/ase-social-network/wiki)  

## 🛠️ Setup Instructions

### Prerequisites
- Ensure **Docker** and **docker-compose** are installed
- you should have terminal to execute local .sh scripts (On Windows, Cygwin compatible terminal, on Linux and MacOS you don't need anything)
  - Be aware that if you want to run the script to setup the repository you SHOULD be in a POSIX terminal, otherwise you won't see possible error messages from error scripts.
  - This issue can occur on windows, when starting the script from init terminal, however bash takes over the execution
- Prepare the environment variables:
  ```bash
  cp .env.example .env
  ```
  Edit `.env` to include your secrets.

### Initialization
- Run the initialization script:
  ```bash
  ./init.sh
  ```
  This sets up the entire environment.

- If you encounter issues or if dependencies in the microservices have changed you can force a rebuild with:
  ```bash
  ./init.sh -b
  ```

- if you want to see logs from the bash script and you are using powershell, you need to add flag `--ps` to the script, like this:
  ```bash
  ./init.sh -p
  ```

- In case of initialization of desired environment you can use `<test/dev>` as an option to the script, like this:
  ```bash
  ./init.sh <test/dev>
  ```

### Local Development without initialization script
- To start local development without the need for manual setups
 use:
  ```bash
  docker compose -f docker-compose.base.yml -f docker-compose.dev.yml -f docker-compose.support.yml up
  ```

### Access Points
- **Main Application:** <http://localhost:8000/>
- **Kong Admin:** <http://localhost:8002/>

### Shutdown
- Turn off all infrastructure components with:
  ```bash
  ./down.sh
  ```

### Swagger Documentation
- Each microservice is equipped with Swagger documentation accessible at the `/docs` endpoint for that specific service.



## 🔄 What Does `./init.sh` Do?
- Creates a Docker network.
- Launches microservices and databases defined in `docker-compose.base.yml`.
- Starts necessary infrastructure such as Kong
 Grafana
 and Loki as defined in `docker-compose.support.yml`.
- Exposes development ports as specified in `docker-compose.dev.yml`.
- Optionally
 the `-b` flag triggers a build of all Docker compose files
 useful for integrating new pip dependencies.

## 🛠️ How to Create a New Microservice?
- Create a new folder in the main repository.
- Add a `Dockerfile` in this new directory.
- Update `docker-compose.yml` with the new service and its dependencies
 such as the database.
- Add the service configuration to `kong/config/kong.yml` for routing and service discovery.

## 🔧 Development Tips
- Python development is facilitated through connected volumes
 with live-refresh enabled.
- When adding pip packages
 rebuild the container using the `--no-cache` flag to ensure new packages are installed immediately, otherwise `-b` flag for unit should be enough:
  ```bash
  docker compose -f docker-compose.base.yml -f docker-compose.dev.yml build --no-cache
  ```
- If Kong configurations are modified in `kong.yml`
 SSH into the Kong container and execute:
  ```bash
  kong reload
  ```

## 🧪 Testing
- Execute unit tests for a specific microservice:
  ```bash
  ./run_tests.sh --unit-tests <ms>
  ```