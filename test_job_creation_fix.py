#!/usr/bin/env python3
"""
Test script to verify the job creation remote_type fix
"""
import requests
import json

# Test data that matches what Flutter sends
test_job_data = {
    "title": "Test Job Remote Type Fix",
    "description": "This is a test job to verify remote_type handling",
    "company": 1,  # Will be mapped to company_id
    "location": "Remote",
    "job_type": "full_time",
    "experience_level": "entry",
    "is_remote": True,
    "remote_type": "remote",  # This should be handled properly now
    "status": "active",
    "is_active": True,
    "is_featured": False,
    "salary_currency": "USD",
    "salary_min": 50000,
    "salary_max": 80000,
    "requirements": "Python, Django",
    "responsibilities": "Develop and maintain backend services"
}

def test_job_creation():
    """Test job creation with proper remote_type handling"""
    url = "http://localhost:8000/api/jobs/create/"
    
    # First, get a valid token (you might need to adjust this)
    login_url = "http://localhost:8000/api/auth/login/"
    login_data = {
        "username": "testuser",  # Adjust as needed
        "password": "testpass123"
    }
    
    print("🔍 Testing job creation with remote_type fix...")
    print(f"📋 Job data: {json.dumps(test_job_data, indent=2)}")
    
    try:
        # Try to login first
        login_response = requests.post(login_url, json=login_data)
        if login_response.status_code == 200:
            token = login_response.json().get('access_token')
            headers = {'Authorization': f'Bearer {token}'}
            print("✅ Authentication successful")
        else:
            print("⚠️ Using request without authentication (may fail)")
            headers = {}
        
        # Create the job
        response = requests.post(url, json=test_job_data, headers=headers)
        
        print(f"📡 Response status: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Job created successfully! remote_type fix is working!")
            return True
        else:
            print(f"❌ Job creation failed with status {response.status_code}")
            if "remote_type" in response.text:
                print("🔍 remote_type still causing issues")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    test_job_creation()
