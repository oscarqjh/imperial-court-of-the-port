"""
Debug script to test progress updates in detail.
"""

import requests
import time
import json

def test_detailed_progress():
    """Test detailed progress updates from Celery tasks."""
    
    base_url = "http://localhost:8000"
    
    print("🔍 Testing Detailed Progress Updates")
    print("=" * 40)
    
    # Submit a job
    print("\n1. Submitting a job...")
    submit_response = requests.post(
        f"{base_url}/incident/run",
        data={"incident_text": "Debug test for progress tracking"}
    )
    
    if submit_response.status_code != 200:
        print(f"❌ Failed to submit job: {submit_response.status_code}")
        print(submit_response.text)
        return
    
    job_data = submit_response.json()
    run_id = job_data["run_id"]
    print(f"✅ Job submitted successfully: {run_id}")
    
    # Poll for detailed progress updates
    print(f"\n2. Polling for detailed progress updates...")
    poll_count = 0
    max_polls = 20
    seen_steps = set()
    
    while poll_count < max_polls:
        poll_count += 1
        time.sleep(1)  # Poll more frequently to catch updates
        
        poll_response = requests.get(f"{base_url}/incident/run/{run_id}")
        if poll_response.status_code != 200:
            print(f"❌ Poll {poll_count}: Failed with {poll_response.status_code}")
            continue
        
        status_data = poll_response.json()
        status = status_data['status']
        progress = status_data.get('progress', 0)
        current_step = status_data.get('current_step', 'Unknown')
        
        # Only print if we see a new step
        step_key = f"{progress}%-{current_step}"
        if step_key not in seen_steps:
            seen_steps.add(step_key)
            print(f"🔄 Poll {poll_count}: Status = {status} ({progress}%) - {current_step}")
        
        if status in ['completed', 'failed']:
            if status == 'completed':
                print(f"✅ Job completed successfully!")
                # Print the final result summary
                if 'result' in status_data and 'incident_analysis' in status_data['result']:
                    analysis = status_data['result']['incident_analysis']
                    print(f"📊 Final Analysis: {analysis.get('incident_type', 'N/A')} - {analysis.get('severity', 'N/A')}")
            else:
                print(f"❌ Job failed: {status_data.get('error', 'Unknown error')}")
            break
    
    print(f"\n✅ Debug test completed! Seen {len(seen_steps)} unique progress steps:")
    for step in sorted(seen_steps):
        print(f"   - {step}")

if __name__ == "__main__":
    test_detailed_progress()
