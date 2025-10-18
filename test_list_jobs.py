"""
Test the list_jobs endpoint to verify it works with the Celery-based implementation.
"""

import requests
import json
import time

def test_list_jobs_endpoint():
    """Test the /incident/jobs endpoint."""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing List Jobs Endpoint")
    print("=" * 40)
    
    try:
        # First, submit a test job so we have something to list
        print("\n1. Submitting a test job first...")
        
        test_incident = {
            "incident_type": "test_incident",
            "severity": "low",
            "payload": {
                "incident_text": "Test incident for list_jobs verification",
                "timestamp": time.time(),
                "source": "api_test"
            }
        }
        
        submit_response = requests.post(
            f"{base_url}/incident/run",
            json=test_incident
        )
        
        if submit_response.status_code == 200:
            job_data = submit_response.json()
            test_run_id = job_data["run_id"]
            print(f"✅ Test job submitted: {test_run_id}")
        else:
            print(f"⚠️ Could not submit test job: {submit_response.status_code}")
            test_run_id = None
        
        # Wait a moment for the job to be registered
        time.sleep(2)
        
        # Now test the list jobs endpoint
        print(f"\n2. Testing /incident/jobs endpoint...")
        
        response = requests.get(f"{base_url}/incident/jobs?limit=10")
        
        if response.status_code == 200:
            jobs_data = response.json()
            print(f"✅ List jobs successful!")
            print(f"📊 Response structure: {list(jobs_data.keys())}")
            
            if "jobs" in jobs_data:
                jobs = jobs_data["jobs"]
                print(f"📋 Found {len(jobs)} jobs")
                
                if jobs:
                    print(f"\n📄 Job details:")
                    for i, job in enumerate(jobs[:3]):  # Show first 3 jobs
                        print(f"  Job {i+1}:")
                        print(f"    Run ID: {job.get('run_id', 'N/A')}")
                        print(f"    Status: {job.get('status', 'N/A')}")
                        print(f"    Created: {job.get('created_at', 'N/A')}")
                        print(f"    Progress: {job.get('progress', 0)}%")
                        print(f"    Current Step: {job.get('current_step', 'N/A')}")
                        
                        # Check if our test job is in the list
                        if test_run_id and job.get('run_id') == test_run_id:
                            print(f"    🎯 Found our test job!")
                        print()
                        
                    if len(jobs) > 3:
                        print(f"  ... and {len(jobs) - 3} more jobs")
                        
                else:
                    print(f"📝 No jobs found in the list")
                    
            else:
                print(f"❌ Unexpected response format: {jobs_data}")
                
            return True
            
        else:
            print(f"❌ List jobs failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        return False

def test_individual_job_status():
    """Test getting individual job status for comparison."""
    
    print(f"\n🔍 Testing individual job status...")
    
    # Submit a job and immediately check its status
    base_url = "http://localhost:8000"
    
    test_incident = {
        "incident_type": "status_test",
        "severity": "medium", 
        "payload": {
            "incident_text": "Quick status test incident",
            "timestamp": time.time()
        }
    }
    
    try:
        submit_response = requests.post(f"{base_url}/incident/run", json=test_incident)
        
        if submit_response.status_code == 200:
            job_data = submit_response.json()
            run_id = job_data["run_id"]
            print(f"✅ Job submitted: {run_id}")
            
            # Get individual status
            status_response = requests.get(f"{base_url}/incident/run/{run_id}")
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"✅ Individual status retrieved:")
                print(f"    Status: {status_data.get('status')}")
                print(f"    Progress: {status_data.get('progress', 0)}%")
                print(f"    Step: {status_data.get('current_step', 'N/A')}")
                return True
            else:
                print(f"❌ Individual status failed: {status_response.status_code}")
                return False
        else:
            print(f"❌ Job submission failed: {submit_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Individual status test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting list_jobs endpoint tests...\n")
    
    # Test the list jobs endpoint
    list_success = test_list_jobs_endpoint()
    
    # Test individual job status for comparison
    individual_success = test_individual_job_status()
    
    print(f"\n🏁 Test Results:")
    print(f"  List Jobs Endpoint: {'✅ PASS' if list_success else '❌ FAIL'}")
    print(f"  Individual Status:  {'✅ PASS' if individual_success else '❌ FAIL'}")
    
    if list_success and individual_success:
        print(f"\n🎉 All tests passed! The list_jobs endpoint is working.")
    else:
        print(f"\n💥 Some tests failed. Check the backend logs for details.")
