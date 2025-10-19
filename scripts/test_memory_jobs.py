#!/usr/bin/env python3
"""Test script for in-memory job management."""

import sys
import json
from datetime import datetime
from typing import NamedTuple

# Add the app directory to Python path
sys.path.append('.')

from app.job_manager import CeleryJobManager, JobInfo, JobStatus

def test_memory_jobs():
    """Test the in-memory job management system."""
    print("🧪 Testing in-memory job management...")
    
    # Create job manager
    manager = CeleryJobManager()
    
    # Test listing empty jobs
    print('\n📋 Testing empty jobs list...')
    jobs = manager.list_jobs()
    print(f'Empty jobs result: {json.dumps(jobs, indent=2, default=str)}')
    
    # Import JobInfo from the module
    # from app.job_manager import JobInfo  # Already imported above
    
    # Create test job
    test_job = JobInfo(
        run_id='test-123',
        celery_task_id='test-123',
        status=JobStatus.QUEUED,
        created_at=datetime.now(),
        incident_text='Test incident for verification...',
        result=None
    )
    
    # Manually add to memory
    manager._jobs['test-123'] = test_job
    manager._job_order.append('test-123')
    
    print('\n📊 Testing with one job in memory...')
    jobs = manager.list_jobs()
    print(f'Jobs with test entry: {json.dumps(jobs, indent=2, default=str)}')
    
    # Test submit_job method (without actual Celery)
    print('\n📤 Testing submit_job method...')
    try:
        # This will fail because Celery isn't running, but we can see if the memory part works
        run_id = manager.submit_job("Test incident text for memory storage")
        print(f'✅ Submit job returned run_id: {run_id}')
        
        # Check if it was stored in memory
        if run_id in manager._jobs:
            print(f'✅ Job {run_id} found in memory')
            print(f'   Job info: {manager._jobs[run_id]}')
        else:
            print(f'❌ Job {run_id} NOT found in memory')
            
    except Exception as e:
        print(f'⚠️ Submit job failed (expected if Celery not running): {e}')
        # Check memory anyway
        print(f'📦 Current jobs in memory: {len(manager._jobs)}')
        
    print('\n🏁 Test completed!')

if __name__ == '__main__':
    test_memory_jobs()
