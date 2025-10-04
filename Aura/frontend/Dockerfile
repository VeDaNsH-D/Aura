# --- Stage 1: Build Stage ---
# Use a Node.js image to build the React static files
FROM node:18-alpine AS builder

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package.json ./
COPY package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application source code
COPY . .

# Build the React application for production
RUN npm run build


# --- Stage 2: Production Stage ---
# Use a lightweight Nginx image to serve the static files
FROM nginx:1.23-alpine

# Copy the built static files from the builder stage to the Nginx public directory
COPY --from=builder /app/build /usr/share/nginx/html

# Copy the custom Nginx configuration file
# This is important for handling client-side routing in a Single Page Application (SPA)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# The default Nginx command will start the server automatically
CMD ["nginx", "-g", "daemon off;"]