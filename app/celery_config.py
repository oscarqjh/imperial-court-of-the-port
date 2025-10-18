"""
Celery configuration for Imperial Court incident processing.
"""
import os
from celery import Celery

# Redis Cloud connection URL with authentication
redis_url = os.getenv("CELERY_BROKER_URL", "redis://default:7VbDuaP8oaA1ldV2SMBXOk85fL5BHarS@redis-15612.c92.us-east-1-3.ec2.redns.redis-cloud.com:15612/0")

# Create Celery app
celery_app = Celery(
    "imperial_court",
    broker=redis_url,
    backend=redis_url,
    include=["app.celery_tasks"]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    # Remove task routing to use default queue
    # task_routes={
    #     "app.celery_tasks.process_incident": {"queue": "incidents"},
    # },
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_max_tasks_per_child=50,
)
