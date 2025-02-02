

# Use the official Node.js image as a base
FROM node:latest

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the container
COPY doc-manager-ui/package.json doc-manager-ui/package-lock.json ./

# Install dependencies
RUN npm install

# Copy the entire app to the container
COPY doc-manager-ui/ ./

# Build the static files
RUN npm run build

# Install `serve` to serve the static files
RUN npm install -g serve

# Expose port 3000
EXPOSE 3000

# Start the static file server
CMD ["serve", "-s", "build", "-l", "3000"]
