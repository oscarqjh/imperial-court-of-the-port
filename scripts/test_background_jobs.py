"""
Test script for the background job system.
"""
import asyncio
import requests
import time
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_background_jobs():
    """Test the background job submission and polling."""
    
    print("🧪 Testing Background Job System")
    print("=" * 50)
    
    # Test 1: Submit a job
    print("\n1️⃣ Submitting incident job...")
    incident_data = {"incident_text": "Test container issue with MSKU1234567 - urgent container missing from port"}
    
    response = requests.post(f"{BASE_URL}/incident/run", data=incident_data)
    if response.status_code != 200:
        print(f"❌ Failed to submit job: {response.status_code} - {response.text}")
        return
    
    job_response = response.json()
    run_id = job_response["run_id"]
    print(f"✅ Job submitted successfully!")
    print(f"   Run ID: {run_id}")
    print(f"   Status: {job_response['status']}")
    print(f"   Created: {job_response['created_at']}")
    
    # Test 2: Poll for status with more frequent checks
    print(f"\n2️⃣ Polling job status for {run_id}...")
    
    max_polls = 60  # Poll for up to 60 seconds
    poll_count = 0
    
    while poll_count < max_polls:
        response = requests.get(f"{BASE_URL}/incident/run/{run_id}")
        if response.status_code != 200:
            print(f"❌ Failed to get job status: {response.status_code}")
            break
            
        status_data = response.json()
        status_msg = f"   Poll {poll_count + 1}: Status = {status_data['status']}"
        
        # Show progress if available
        if status_data.get("progress") is not None:
            status_msg += f" ({status_data['progress']}%)"
        if status_data.get("current_step"):
            status_msg += f" - {status_data['current_step']}"
            
        print(status_msg)
        
        if status_data["status"] in ["completed", "failed"]:
            print(f"✅ Job finished with status: {status_data['status']}")
            if status_data["status"] == "completed":
                print(f"   Started: {status_data['started_at']}")
                print(f"   Completed: {status_data['completed_at']}")
                if status_data.get("result"):
                    result = status_data["result"]
                    print(f"   Result preview: {str(result)[:200]}...")
            elif status_data["status"] == "failed":
                print(f"   Error: {status_data.get('error', 'Unknown error')}")
            break
            
        time.sleep(2)  # Wait 2 seconds between polls to see status changes
        poll_count += 1
    
    if poll_count >= max_polls:
        print("⏰ Polling timeout - job may still be running")
    
    # Test 3: List all jobs
    print(f"\n3️⃣ Listing all jobs...")
    response = requests.get(f"{BASE_URL}/incident/jobs")
    if response.status_code == 200:
        jobs_data = response.json()
        print(f"✅ Found {len(jobs_data['jobs'])} jobs:")
        for job in jobs_data["jobs"][:3]:  # Show first 3 jobs
            print(f"   - {job['run_id']}: {job['status']} (created: {job['created_at'][:19]})")
    else:
        print(f"❌ Failed to list jobs: {response.status_code}")
    
    print("\n🎯 Test completed!")

if __name__ == "__main__":
    try:
        test_background_jobs()
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Test failed: {e}")
