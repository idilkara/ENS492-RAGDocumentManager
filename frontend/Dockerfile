# Use the official Node.js image to build the React app
FROM node:latest AS build

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json for better caching
COPY doc-manager-ui/package.json doc-manager-ui/package-lock.json ./

# Install dependencies
RUN npm install

# Copy the entire app to the container
COPY doc-manager-ui/ ./

# Fix permissions issue
RUN chmod -R 777 node_modules

# Build the React app
RUN npm run build  # This will generate the build files in the build/ directory

# Use the official Nginx image to serve the static files
FROM nginx:latest

# Copy the build files from the build stage into Nginx's default directory
COPY --from=build /usr/src/app/build /usr/share/nginx/html

# Expose port 80 for Nginx to serve the app
EXPOSE 80

# Run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
