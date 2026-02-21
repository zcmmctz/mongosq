FROM node:20-alpine AS frontend-build

# Set working directory
WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy frontend source code
COPY frontend/ .

# Build frontend
RUN npm run build

# Backend stage
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend files
COPY server/ .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Copy built frontend from previous stage
COPY --from=frontend-build /app/frontend/dist/spa /app/static

# Create a simple entrypoint script
RUN echo '#!/bin/bash\n\n# Start the backend server\nuvicorn main:app --host 0.0.0.0 --port 22222 --reload' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 22222

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]