"""
Simple test for list_jobs - just hit the endpoint directly.
"""

import requests

def simple_list_test():
    try:
        print("Testing /incident/jobs endpoint...")
        response = requests.get("http://localhost:8000/incident/jobs")
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
            
            if 'jobs' in data:
                job_count = len(data['jobs'])
                print(f"✅ Found {job_count} jobs")
                
                if job_count > 0:
                    first_job = data['jobs'][0]
                    print(f"First job: {first_job}")
                else:
                    print("No jobs in the list")
            else:
                print("❌ No 'jobs' key in response")
        else:
            print(f"❌ Failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    simple_list_test()
