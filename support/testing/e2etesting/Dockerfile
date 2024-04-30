FROM cypress/included:latest

WORKDIR /app

COPY package*.json ./
RUN npm install --ignore-scripts

COPY cypress/ ./cypress
