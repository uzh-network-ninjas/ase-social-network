# ms-frontend

## Overview
The ms-frontend microservice is responsible for delivering the interactive web application to users. It serves as the primary interface for user interaction.

General developer setup instructions can be found [here](https://github.com/uzh-network-ninjas/ase-social-network/wiki/Developer-Setup).

For more detailed information about the ms-frontend, visit our [wiki page](https://github.com/uzh-network-ninjas/ase-social-network/wiki/Microservices#ms-frontend-).

## Guidelines

Before submitting a pull request, ensure your changes adhere to coding standards and style by running ESLint and Prettier. This helps maintain code quality and consistency across the project.

## Setup

While development in a Docker environment is recommended for consistency across setups (details in the [Developer Setup Guide](https://github.com/uzh-network-ninjas/ase-social-network/wiki/Developer-Setup)), it is also possible to run the ms-frontend locally without Docker using the following commands:

## Project Setup
To use the project locally, execute following commands in the `ms-frontend` folder:

### Installing Dependencies

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

## Format with [Prettier](https://prettier.io/)

```sh
npm run format
```
