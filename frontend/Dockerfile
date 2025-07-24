# Use lightweight Node.js 18 image as the build environment
FROM node:18-alpine AS build-stage

# Set working directory inside the container to /app
WORKDIR /app

# Copy package.json and package-lock.json files to the working directory
COPY package*.json ./

# Install all Node.js dependencies defined in package.json
RUN npm install

# Copy the rest of the frontend source code to the container
COPY . .

# Build the frontend application, creating optimized static files
RUN npm run build

# Use lightweight Nginx image to serve the built frontend files
FROM nginx:alpine

# Copy built static files from the build-stage to Nginx's default directory
COPY --from=build-stage /app/build /usr/share/nginx/html

# Expose port 80 for HTTP traffic
EXPOSE 80

# Run Nginx in the foreground (non-daemon mode) to keep the container running
CMD ["nginx", "-g", "daemon off;"]