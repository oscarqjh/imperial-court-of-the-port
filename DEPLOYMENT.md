# Imperial Court Backend - Containerization & Deployment Guide

## 📋 Overview

This guide covers containerizing and deploying the Imperial Court FastAPI + Celery backend to various cloud platforms.

## 🏗️ Architecture

- **FastAPI**: REST API server
- **Celery**: Background task processing
- **Redis**: Message broker for Celery
- **Supabase**: PostgreSQL database
- **Qdrant**: Vector database for RAG
- **OpenAI**: LLM integration

## 🐳 Local Development with Docker

### Prerequisites

- Docker & Docker Compose installed
- `.env` file with required environment variables

### Quick Start

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Services

- **FastAPI**: http://localhost:8000
- **Celery Flower**: http://localhost:5555 (monitoring)
- **Redis**: localhost:6379

## 🚀 Production Deployment

### 1. Build Production Image

```bash
# Build production image
docker build -t imperial-court-backend:latest .

# Or use the build script
./deploy/build-and-push.sh  # Linux/Mac
# OR
./deploy/build-and-push.bat  # Windows
```

### 2. Environment Configuration

Create production environment files:

```bash
cp .env.example .env.production
# Edit .env.production with production values
```

### 3. Run Production Stack

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## ☁️ Cloud Deployment Options

### Option 1: Container Registry + Kubernetes

1. **Push to Container Registry**:

   ```bash
   # Tag for your registry
   docker tag imperial-court-backend:latest your-registry.com/imperial-court-backend:latest

   # Push to registry
   docker push your-registry.com/imperial-court-backend:latest
   ```

2. **Deploy to Kubernetes**:
   ```bash
   # Update kubernetes.yaml with your registry URL and secrets
   kubectl apply -f deploy/kubernetes.yaml
   ```

### Option 2: Docker Swarm

```bash
# Initialize swarm (if not already done)
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.prod.yml imperial-court
```

### Option 3: Cloud-Specific Deployments

#### AWS ECS

- Use the Dockerfile with AWS ECS
- Configure task definitions for FastAPI and Celery
- Use AWS ElastiCache for Redis
- Use RDS for PostgreSQL

#### Google Cloud Run

- Deploy FastAPI container to Cloud Run
- Use Cloud Tasks for background processing
- Use Cloud SQL for PostgreSQL

#### Azure Container Instances

- Deploy containers to ACI
- Use Azure Service Bus for messaging
- Use Azure Database for PostgreSQL

## 🔧 Configuration

### Required Environment Variables

| Variable            | Description           | Example                             |
| ------------------- | --------------------- | ----------------------------------- |
| `OPENAI_API_KEY`    | OpenAI API key        | `sk-proj-...`                       |
| `QDRANT_URL`        | Qdrant vector DB URL  | `https://xyz.qdrant.io:6333`        |
| `QDRANT_API_KEY`    | Qdrant API key        | `eyJhbGci...`                       |
| `SUPABASE_DB_URL`   | PostgreSQL connection | `postgres://user:pass@host:port/db` |
| `CELERY_BROKER_URL` | Redis URL for Celery  | `redis://host:port/0`               |
| `MOCK_MODE`         | Enable mock mode      | `false`                             |

### Optional Variables

| Variable                 | Description            | Default                  |
| ------------------------ | ---------------------- | ------------------------ |
| `EMBED_MODEL`            | Embedding model        | `text-embedding-3-small` |
| `QDRANT_COLLECTION`      | Qdrant collection name | `imperial_court_kb`      |
| `CREWAI_TRACING_ENABLED` | Enable CrewAI tracing  | `false`                  |

## 📊 Monitoring & Logging

### Health Checks

- **Liveness**: `GET /health`
- **Readiness**: `GET /health/ready`

### Celery Monitoring

- **Flower Dashboard**: Port 5555
- **Task Monitoring**: Check Redis for task states

### Logs

```bash
# Docker Compose logs
docker-compose logs -f [service-name]

# Kubernetes logs
kubectl logs -f deployment/imperial-court-fastapi
kubectl logs -f deployment/imperial-court-celery-worker
```

## 🔒 Security Considerations

1. **Secrets Management**: Use proper secret management systems
2. **Network Security**: Configure firewalls and VPCs
3. **Image Security**: Scan images for vulnerabilities
4. **Environment Isolation**: Separate dev/staging/prod environments
5. **TLS/SSL**: Enable HTTPS in production

## 📈 Scaling

### Horizontal Scaling

- **FastAPI**: Scale replicas based on CPU/memory usage
- **Celery Workers**: Scale based on queue length
- **Redis**: Use Redis Cluster for high availability

### Vertical Scaling

- Adjust CPU/memory limits in Docker/Kubernetes configs
- Monitor resource usage and adjust accordingly

## 🛠️ Troubleshooting

### Common Issues

1. **Container won't start**:

   ```bash
   # Check logs
   docker logs <container-id>

   # Check environment variables
   docker exec -it <container-id> env
   ```

2. **Celery tasks not processing**:

   ```bash
   # Check Redis connectivity
   docker exec -it <container-id> redis-cli -u $CELERY_BROKER_URL ping

   # Check Celery worker status
   docker exec -it <container-id> celery -A app.celery_config.celery_app inspect active
   ```

3. **Database connection issues**:
   ```bash
   # Test database connection
   docker exec -it <container-id> python -c "from app.db import test_connection; test_connection()"
   ```

## 📝 Development Workflow

1. **Local Development**: Use `docker-compose.yml`
2. **Testing**: Run tests in containers
3. **Building**: Use build scripts in `deploy/`
4. **Deployment**: Use appropriate cloud deployment method

## 🔄 CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Build and Deploy
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker image
        run: docker build -t imperial-court-backend .
      - name: Push to registry
        run: |
          docker tag imperial-court-backend $REGISTRY/imperial-court-backend:$GITHUB_SHA
          docker push $REGISTRY/imperial-court-backend:$GITHUB_SHA
```

## 📞 Support

For deployment issues or questions, check:

1. Application logs
2. Container logs
3. Cloud platform documentation
4. This deployment guide
