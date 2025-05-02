# Use the official Node.js image
FROM node:latest

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json first for better caching
COPY doc-manager-ui/package.json doc-manager-ui/package-lock.json ./

# Install dependencies
RUN npm install

# Copy the entire app to the container
COPY doc-manager-ui/ ./

# Fix permissions issue
RUN chmod -R 777 node_modules

# Build the static files
RUN npx react-scripts build  # Using npx ensures the local version is used

# Install `serve` globally
RUN npm install -g serve

# Expose port 3000
EXPOSE 3000

# Start the static file server
CMD ["serve", "-s", "build", "-l", "3000"]
