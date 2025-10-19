@echo off
REM Build and Deploy Script for Imperial Court Backend (Windows)

echo 🏛️ Imperial Court Backend Deployment Script
echo ===========================================

REM Build the Docker image
echo 📦 Building Docker image...
docker build -t imperial-court-backend:latest .

REM Tag for deployment (modify registry URL as needed)
set REGISTRY_URL=your-registry.com
for /f "tokens=*" %%i in ('powershell -Command "Get-Date -Format 'yyyyMMdd-HHmmss'"') do set TIMESTAMP=%%i
set IMAGE_TAG=imperial-court-backend:%TIMESTAMP%

echo 🏷️ Tagging image: %IMAGE_TAG%
docker tag imperial-court-backend:latest %REGISTRY_URL%/%IMAGE_TAG%
docker tag imperial-court-backend:latest %REGISTRY_URL%/imperial-court-backend:latest

REM Push to registry
echo 📤 Pushing to registry...
docker push %REGISTRY_URL%/%IMAGE_TAG%
docker push %REGISTRY_URL%/imperial-court-backend:latest

echo ✅ Build and push completed!
echo Image: %REGISTRY_URL%/%IMAGE_TAG%
echo Latest: %REGISTRY_URL%/imperial-court-backend:latest

pause
