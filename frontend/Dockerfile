# Build stage
FROM node:18-alpine AS builder
WORKDIR /app

# Copy package files first
COPY package*.json ./

# Install all dependencies (including devDependencies like Vite)
RUN npm install

# Copy the rest of the source code (Docker will now safely ignore local node_modules via .dockerignore)
COPY . .

# Build the project using npx
RUN npx vite build

# Production stage using Nginx
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html

# COPY custom nginx configuration to handle SPA client-side routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]