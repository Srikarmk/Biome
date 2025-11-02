# Frontend Dockerfile for Biome Coaching Agent
# Multi-stage build for optimized production bundle

# Stage 1: Build the React application
FROM node:18-alpine AS build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY src/ ./src/
COPY public/ ./public/
COPY tailwind.config.js .
COPY tsconfig.json .
COPY postcss.config.js .

# Build for production
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Copy built files from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Create nginx configuration for SPA routing
# Note: For separate Cloud Run deployments, remove the /api proxy section
# and set REACT_APP_API_URL env var in frontend build instead
RUN echo 'server { \
    listen 8080; \
    server_name _; \
    root /usr/share/nginx/html; \
    index index.html; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

# Cloud Run uses PORT environment variable
EXPOSE 8080

# Start nginx
CMD ["nginx", "-g", "daemon off;"]

