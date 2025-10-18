# Celery Background Job Setup Guide

## Prerequisites

This setup uses Redis Cloud as the message broker and result backend for Celery.

**Redis Cloud Connection**: `redis-15612.c92.us-east-1-3.ec2.redns.redis-cloud.com:15612`

### Alternative Local Redis Setup

If you want to use local Redis instead:

#### Option 1: Using Docker

```bash
docker run -d -p 6379:6379 redis:alpine
```

#### Option 2: Install Redis natively

- **Windows**: Download from https://github.com/microsoftarchive/redis/releases
- **Linux/Mac**: `sudo apt install redis-server` or `brew install redis`

## Starting the System

**Note**: Redis Cloud is already configured and ready to use!

### 1. Start Celery Worker

Open a new terminal and run:

```bash
cd c:\Users\User\Documents\NTU_WORK\imperial-court-of-the-port
C:/Users/User/Documents/NTU_WORK/imperial-court-of-the-port/.venv/Scripts/python.exe start_celery_worker.py
```

Or using celery command directly:

```bash
C:/Users/User/Documents/NTU_WORK/imperial-court-of-the-port/.venv/Scripts/celery.exe -A app.celery_config worker --loglevel=info --concurrency=2 --queues=incidents,celery
```

### 2. Start FastAPI Server (if not already running)

```bash
C:/Users/User/Documents/NTU_WORK/imperial-court-of-the-port/.venv/Scripts/python.exe -m uvicorn app.main:app --port 8000 --reload
```

### 3. Test the System

```bash
C:/Users/User/Documents/NTU_WORK/imperial-court-of-the-port/.venv/Scripts/python.exe test_background_jobs.py
```

## How It Works

1. **Job Submission**: POST to `/incident/run` submits the task to Celery and returns immediately with a `run_id`
2. **Background Processing**: Celery worker picks up the task and processes it asynchronously
3. **Status Polling**: GET `/incident/run/{run_id}` returns real-time status including:

   - `queued` - Task is waiting to be picked up
   - `processing` - Task is actively running
   - `completed` - Task finished successfully
   - `failed` - Task encountered an error

4. **Progress Updates**: During processing, you'll see progress percentage and current step information

## Environment Variables

You can customize the setup with these environment variables:

```bash
# Redis Cloud connection (already configured)
CELERY_BROKER_URL=redis://redis-15612.c92.us-east-1-3.ec2.redns.redis-cloud.com:15612/0
CELERY_RESULT_BACKEND=redis://redis-15612.c92.us-east-1-3.ec2.redns.redis-cloud.com:15612/0

# If using authentication (add if needed)
# CELERY_BROKER_URL=redis://:password@redis-15612.c92.us-east-1-3.ec2.redns.redis-cloud.com:15612/0

# Enable/disable mock mode
MOCK_MODE=false
```

## Monitoring Celery

### Check worker status:

```bash
C:/Users/User/Documents/NTU_WORK/imperial-court-of-the-port/.venv/Scripts/celery.exe -A app.celery_config inspect active
```

### Monitor tasks:

```bash
C:/Users/User/Documents/NTU_WORK/imperial-court-of-the-port/.venv/Scripts/celery.exe -A app.celery_config flower
```

Then visit http://localhost:5555 for web monitoring.

## Troubleshooting

**Redis Connection Error**:

- Make sure Redis is running on port 6379
- Check firewall settings

**Task Stuck in PENDING**:

- Ensure Celery worker is running
- Check worker logs for errors

**Import Errors**:

- Make sure all dependencies are installed
- Check Python path configuration

**Task Fails Immediately**:

- Check worker logs for detailed error messages
- Verify database connections and environment variables
