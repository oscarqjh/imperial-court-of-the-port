"""
Test the file upload API to verify it works with the new frontend format.
"""

import requests
import json

def test_file_upload_submission():
    """Test submitting an incident with file upload format."""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing File Upload API Format")
    print("=" * 40)
    
    # Test data that matches what the new frontend sends
    test_data = {
        "incident_type": "uploaded_content",
        "severity": "medium", 
        "payload": {
            "incident_text": """=== File: incident_report.txt ===
System Error: Container allocation failure
Time: 2025-10-18 14:30:00
Affected System: Container Management System
Error Code: CMS-500-ALLOCATION
Description: Unable to allocate container berth due to conflicting reservations
Impact: 3 vessels delayed, estimated delay 2-4 hours

=== Additional Information ===
This appears to be a recurring issue with the berth allocation algorithm.
Previous similar incidents: INC-2025-001, INC-2025-007
Temporary workaround applied: Manual berth assignment""",
            "uploaded_files": [
                {
                    "name": "incident_report.txt",
                    "type": "text/plain",
                    "size": 1024
                }
            ],
            "timestamp": "2025-10-18T14:30:00Z",
            "source": "web_interface"
        }
    }
    
    try:
        print("\n1. Submitting incident...")
        print(f"📝 Incident Type: {test_data['incident_type']}")
        print(f"⚖️ Severity: {test_data['severity']}")
        print(f"📄 Files: {len(test_data['payload']['uploaded_files'])}")
        
        response = requests.post(
            f"{base_url}/incident/run",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            job_data = response.json()
            run_id = job_data["run_id"]
            print(f"✅ Submission successful!")
            print(f"📋 Run ID: {run_id}")
            print(f"📊 Status: {job_data['status']}")
            
            # Test polling the status
            print(f"\n2. Polling status...")
            poll_response = requests.get(f"{base_url}/incident/run/{run_id}")
            
            if poll_response.status_code == 200:
                status_data = poll_response.json()
                print(f"✅ Status poll successful!")
                print(f"📊 Status: {status_data['status']}")
                print(f"🔄 Progress: {status_data.get('progress', 0)}%")
                print(f"📝 Current Step: {status_data.get('current_step', 'Unknown')}")
                
                return True
            else:
                print(f"❌ Status poll failed: {poll_response.status_code}")
                print(f"Response: {poll_response.text}")
                return False
                
        else:
            print(f"❌ Submission failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        return False

if __name__ == "__main__":
    success = test_file_upload_submission()
    if success:
        print(f"\n🎉 File upload API test completed successfully!")
        print("✅ Frontend format is compatible with backend")
    else:
        print(f"\n💥 File upload API test failed!")
        print("❌ Check backend endpoint or data format")
