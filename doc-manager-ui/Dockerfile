# Use the official Node.js image as a base
FROM node:24-alpine

# Set the working directory inside the container
WORKDIR /usr/src/app

# Install the dependencies globally (optional)
RUN npm install -g serve

# Install React app dependencies dynamically when the container starts
CMD ["sh", "-c", "npm install && npm start"]
