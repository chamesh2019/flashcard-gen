# syntax=docker/dockerfile:1

# Stage 1: Build the Vue.js frontend
FROM node:lts-alpine AS frontend-builder
WORKDIR /app/frontend
COPY package.json yarn.lock ./
RUN yarn install
COPY . .
RUN yarn build

# Stage 2: Python backend base
FROM python:3.13-slim AS python-base
WORKDIR /app/backend

# Install dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY backend/app.py ./
COPY backend/functions/ ./functions/

# Stage 3: Nginx
FROM nginx:stable-alpine AS production
WORKDIR /app

# Copy built frontend from frontend-builder stage
COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html

# Copy Nginx configuration
COPY backend/nginx.conf /etc/nginx/conf.d/default.conf

# Copy SSL certificates (ensure these are correctly mounted in compose.yaml)
# These paths are placeholders for where compose.yaml will mount them
COPY backend/certificates/cert.pem /etc/ssl/certs/cert.pem
COPY backend/certificates/key.pem /etc/ssl/private/key.pem

# Expose ports (Nginx will listen on 80 and 443)
EXPOSE 80
EXPOSE 443

# Nginx will be started by the CMD in compose.yaml or its default behavior
# The backend will be started by gunicorn in compose.yaml

# For the backend service in compose.yaml, you'll use python-base
# and run gunicorn. For the nginx service, you'll use this production stage.
