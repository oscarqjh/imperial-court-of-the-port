"""
Start Celery worker for Imperial Court incident processing.
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.celery_config import celery_app

if __name__ == "__main__":
    # Start the worker
    celery_app.start([
        "worker",
        "--loglevel=info",
        "--pool=solo",
        "--concurrency=4",
        "--queues=incidents,celery",
        "--hostname=worker@%h",
        "-E"
    ])
