#!/bin/bash

# Build and Deploy Script for Imperial Court Backend

set -e

echo "🏛️ Imperial Court Backend Deployment Script"
echo "==========================================="

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Build the Docker image
echo "📦 Building Docker image..."
docker build -t imperial-court-backend:latest .

# Tag for deployment (modify registry URL as needed)
REGISTRY_URL="your-registry.com"  # Replace with your container registry
IMAGE_TAG="imperial-court-backend:$(date +%Y%m%d-%H%M%S)"

echo "🏷️ Tagging image: $IMAGE_TAG"
docker tag imperial-court-backend:latest $REGISTRY_URL/$IMAGE_TAG
docker tag imperial-court-backend:latest $REGISTRY_URL/imperial-court-backend:latest

# Push to registry
echo "📤 Pushing to registry..."
docker push $REGISTRY_URL/$IMAGE_TAG
docker push $REGISTRY_URL/imperial-court-backend:latest

echo "✅ Build and push completed!"
echo "Image: $REGISTRY_URL/$IMAGE_TAG"
echo "Latest: $REGISTRY_URL/imperial-court-backend:latest"
