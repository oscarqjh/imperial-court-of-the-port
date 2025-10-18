"""
Test script to validate job persistence across server reloads.
"""

import requests
import time
import json

def test_job_persistence():
    """Test that jobs persist even when the server reloads."""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Job Persistence Across Server Reloads")
    print("=" * 50)
    
    # Step 1: Submit a job
    print("\n1. Submitting a job...")
    submit_response = requests.post(
        f"{base_url}/incident/run",
        data={"incident_text": "Test incident for persistence validation"}
    )
    
    if submit_response.status_code != 200:
        print(f"❌ Failed to submit job: {submit_response.status_code}")
        print(submit_response.text)
        return
    
    job_data = submit_response.json()
    run_id = job_data["run_id"]
    print(f"✅ Job submitted successfully: {run_id}")
    
    # Step 2: Poll once to get initial status
    print("\n2. Polling job status...")
    poll_response = requests.get(f"{base_url}/incident/run/{run_id}")
    
    if poll_response.status_code != 200:
        print(f"❌ Failed to poll job: {poll_response.status_code}")
        print(poll_response.text)
        return
    
    status_data = poll_response.json()
    print(f"✅ Initial status: {status_data['status']}")
    if status_data.get('progress'):
        print(f"   Progress: {status_data['progress']}%")
    if status_data.get('current_step'):
        print(f"   Step: {status_data['current_step']}")
    
    # Step 3: Instructions for manual reload test
    print(f"\n3. 🔄 MANUAL ACTION REQUIRED:")
    print(f"   - Keep this script running")
    print(f"   - In another terminal, modify any .py file to trigger uvicorn reload")
    print(f"   - OR press Ctrl+C in the uvicorn terminal and restart it")
    print(f"   - Then press Enter here to continue testing...")
    
    input("   Press Enter after server reload...")
    
    # Step 4: Try polling again after reload
    print(f"\n4. Testing job status after server reload...")
    time.sleep(2)  # Give server time to restart
    
    for attempt in range(5):
        try:
            poll_response = requests.get(f"{base_url}/incident/run/{run_id}")
            
            if poll_response.status_code == 200:
                status_data = poll_response.json()
                print(f"✅ Job still exists after reload!")
                print(f"   Status: {status_data['status']}")
                if status_data.get('progress'):
                    print(f"   Progress: {status_data['progress']}%")
                if status_data.get('current_step'):
                    print(f"   Step: {status_data['current_step']}")
                
                # Continue polling until completion or timeout
                print(f"\n5. Continuing to poll until completion...")
                poll_count = 0
                max_polls = 30
                
                while poll_count < max_polls:
                    poll_count += 1
                    time.sleep(2)
                    
                    poll_response = requests.get(f"{base_url}/incident/run/{run_id}")
                    if poll_response.status_code != 200:
                        print(f"❌ Poll {poll_count}: Failed with {poll_response.status_code}")
                        continue
                    
                    status_data = poll_response.json()
                    status = status_data['status']
                    progress = status_data.get('progress', 0)
                    current_step = status_data.get('current_step', 'Unknown')
                    
                    print(f"📊 Poll {poll_count}: Status = {status} ({progress}%) - {current_step}")
                    
                    if status in ['completed', 'failed']:
                        if status == 'completed':
                            print(f"✅ Job completed successfully!")
                            if 'result' in status_data:
                                print(f"📋 Result: {json.dumps(status_data['result'], indent=2)}")
                        else:
                            print(f"❌ Job failed: {status_data.get('error', 'Unknown error')}")
                        break
                        
                    elif status == 'processing' and progress == 100:
                        print("⏳ Processing at 100%, waiting for completion...")
                
                break
                
            elif poll_response.status_code == 404:
                print(f"❌ Job not found after reload (this was the old problem)")
                print(f"   Status code: 404")
                break
            else:
                print(f"⚠️  Attempt {attempt + 1}: Got status {poll_response.status_code}, retrying...")
                time.sleep(3)
                
        except requests.exceptions.ConnectionError:
            print(f"⚠️  Attempt {attempt + 1}: Connection failed, retrying...")
            time.sleep(3)
    
    print(f"\n✅ Persistence test completed!")

if __name__ == "__main__":
    test_job_persistence()
