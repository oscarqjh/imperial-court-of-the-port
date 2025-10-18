"""
Simple test to check if Celery task can run without errors.
"""

import requests
import time

def simple_test():
    """Simple test to submit a job and check basic status."""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Simple Celery Test")
    print("=" * 30)
    
    # Submit a job
    print("\n1. Submitting a job...")
    try:
        submit_response = requests.post(
            f"{base_url}/incident/run",
            data={"incident_text": "Simple test incident"}
        )
        
        if submit_response.status_code != 200:
            print(f"❌ Failed to submit job: {submit_response.status_code}")
            print(submit_response.text)
            return
        
        job_data = submit_response.json()
        run_id = job_data["run_id"]
        print(f"✅ Job submitted successfully: {run_id}")
        
        # Poll a few times to see basic progress
        print("\n2. Basic polling...")
        for i in range(5):
            time.sleep(2)
            
            poll_response = requests.get(f"{base_url}/incident/run/{run_id}")
            if poll_response.status_code != 200:
                print(f"❌ Poll failed with {poll_response.status_code}")
                continue
            
            status_data = poll_response.json()
            status = status_data['status']
            progress = status_data.get('progress', 0)
            current_step = status_data.get('current_step', 'Unknown')
            
            print(f"📊 Poll {i+1}: Status = {status} ({progress}%) - {current_step}")
            
            if status in ['completed', 'failed']:
                if status == 'completed':
                    print(f"✅ Job completed successfully!")
                else:
                    print(f"❌ Job failed: {status_data.get('error', 'Unknown error')}")
                break
        
        print(f"\n✅ Simple test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    simple_test()
