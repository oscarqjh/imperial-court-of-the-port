"""
Simple test to check if Celery worker is processing tasks.
"""
import time
from app.celery_tasks import process_incident
from app.celery_config import celery_app

def test_celery_direct():
    print("🧪 Testing Celery Task Directly")
    print("=" * 40)
    
    # Submit a simple task
    print("1️⃣ Submitting task to Celery...")
    task = process_incident.delay("Test incident for Celery verification")
    print(f"   Task ID: {task.id}")
    print(f"   Initial State: {task.state}")
    
    # Poll task status
    print("\n2️⃣ Polling task status...")
    for i in range(20):  # Poll for 20 seconds
        print(f"   Poll {i+1}: State = {task.state}")
        
        if task.state in ['SUCCESS', 'FAILURE']:
            print(f"✅ Task finished with state: {task.state}")
            if task.state == 'SUCCESS':
                print(f"   Result: {task.result}")
            else:
                print(f"   Error: {task.info}")
            break
        elif task.state == 'PROCESSING':
            if task.info and isinstance(task.info, dict):
                progress = task.info.get('progress', 'Unknown')
                step = task.info.get('current_step', 'Unknown')
                print(f"       Progress: {progress}% - {step}")
        
        time.sleep(1)
    else:
        print("⏰ Polling timeout")
    
    # Check worker status
    print("\n3️⃣ Checking worker status...")
    try:
        inspect = celery_app.control.inspect()
        active_tasks = inspect.active()
        if active_tasks:
            print(f"   Active tasks: {active_tasks}")
        else:
            print("   No active tasks found")
            
        stats = inspect.stats()
        if stats:
            print(f"   Worker stats: {stats}")
        else:
            print("   No workers found or not responding")
    except Exception as e:
        print(f"   Error checking worker status: {e}")

if __name__ == "__main__":
    test_celery_direct()
