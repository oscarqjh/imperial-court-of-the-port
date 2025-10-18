#!/usr/bin/env python3
"""Test the actual API endpoints for job management."""

import requests
import json
import time

# API base URL (adjust if needed)
BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Test the actual API endpoints."""
    print("🧪 Testing API endpoints...")
    
    # Test 1: List jobs (should be empty initially)
    print("\n📋 Testing GET /incident/jobs...")
    try:
        response = requests.get(f"{BASE_URL}/incident/jobs")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Submit a new incident
    print("\n📤 Testing POST /incident/run...")
    incident_data = {
        "incident_type": "test",
        "severity": "medium", 
        "payload": "This is a test incident for API validation"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/incident/run",
            json=incident_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if response.status_code == 200 and "run_id" in result:
            run_id = result["run_id"]
            print(f"✅ Job submitted successfully! Run ID: {run_id}")
            
            # Test 3: Check job status
            print(f"\n🔍 Testing GET /incident/run/{run_id}...")
            time.sleep(1)  # Give it a moment
            
            status_response = requests.get(f"{BASE_URL}/incident/run/{run_id}")
            print(f"Status: {status_response.status_code}")
            print(f"Response: {json.dumps(status_response.json(), indent=2)}")
            
            # Test 4: List jobs again (should show our job)
            print(f"\n📊 Testing GET /incident/jobs again...")
            time.sleep(1)
            
            jobs_response = requests.get(f"{BASE_URL}/incident/jobs")
            print(f"Status: {jobs_response.status_code}")
            jobs_data = jobs_response.json()
            print(f"Response: {json.dumps(jobs_data, indent=2)}")
            
            # Check the jobs array inside the response
            if jobs_data.get("jobs") and len(jobs_data["jobs"]) > 0:
                print(f"✅ Found {len(jobs_data['jobs'])} job(s) in the list!")
                print(f"📋 First job status: {jobs_data['jobs'][0]['status']}")
            else:
                print("❌ Jobs list is still empty")
                
        else:
            print("❌ Job submission failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🏁 API test completed!")

if __name__ == '__main__':
    test_api_endpoints()
