#!/usr/bin/env python3
"""
Test Script to Verify API Fixes
This script tests all the critical endpoints to ensure the fixes are working.
"""

import requests
import json
import time

# Configuration
BASE_URLS = {
    'user': 'http://localhost:8001',
    'job': 'http://localhost:8002', 
    'application': 'http://localhost:8003'
}

def test_user_service():
    """Test user service endpoints"""
    print("🔐 Testing User Service...")
    
    # Generate unique username with timestamp
    import time
    timestamp = int(time.time())
    unique_username = f"testuser_{timestamp}"
    
    # Test registration with correct fields
    register_data = {
        'email': f'test{timestamp}@example.com',
        'username': unique_username,
        'password': 'testpass123',
        'password_confirm': 'testpass123',
        'user_type': 'job_seeker',
        'phone_number': '+1234567890',
        'date_of_birth': '1990-01-01'
    }
    
    try:
        response = requests.post(f"{BASE_URLS['user']}/api/users/register/", json=register_data)
        if response.status_code == 201:
            print("✅ User registration successful")
            user_data = response.json()
            return user_data
        else:
            print(f"❌ User registration failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"💥 User registration error: {e}")
        return None

def test_job_service():
    """Test job service endpoints"""
    print("💼 Testing Job Service...")
    
    try:
        response = requests.get(f"{BASE_URLS['job']}/api/jobs/")
        if response.status_code == 200:
            print("✅ Job listing successful")
            jobs = response.json()
            if jobs:
                return jobs[0]['id']  # Return first job ID
            else:
                print("⚠️ No jobs found")
                return None
        else:
            print(f"❌ Job listing failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"💥 Job service error: {e}")
        return None

def test_application_service_with_auth(token, job_id):
    """Test application service with authentication"""
    print("📝 Testing Application Service with Auth...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test check application status
    try:
        response = requests.get(
            f"{BASE_URLS['application']}/api/applications/check-status/{job_id}/",
            headers=headers
        )
        if response.status_code == 200:
            print("✅ Application status check successful")
            status_data = response.json()
            print(f"   Status: {status_data}")
        else:
            print(f"❌ Application status check failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"💥 Application status check error: {e}")
    
    # Test create application
    application_data = {
        'job_id': job_id,
        'employer_id': 5,  # This should be the job's employer ID
        'cover_letter': 'Test cover letter',
        'expected_salary': 50000.0,
        'availability_date': '2025-01-01'
    }
    
    try:
        response = requests.post(
            f"{BASE_URLS['application']}/api/applications/create/",
            json=application_data,
            headers=headers
        )
        if response.status_code == 201:
            print("✅ Application creation successful")
            app_data = response.json()
            print(f"   Application ID: {app_data['id']}")
        else:
            print(f"❌ Application creation failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"💥 Application creation error: {e}")

def test_application_service_without_auth(job_id):
    """Test application service without authentication (should fail)"""
    print("🚫 Testing Application Service without Auth...")
    
    try:
        response = requests.get(f"{BASE_URLS['application']}/api/applications/check-status/{job_id}/")
        if response.status_code == 401:
            print("✅ Authentication required (as expected)")
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"💥 Error: {e}")

def main():
    """Main test function"""
    print("🧪 Starting API Fixes Test Suite...")
    print("=" * 50)
    
    # Test 1: User Service
    user_data = test_user_service()
    if not user_data:
        print("❌ Cannot proceed without user registration")
        return
    
    # Test 2: Job Service
    job_id = test_job_service()
    if not job_id:
        print("❌ Cannot proceed without job data")
        return
    
    print(f"📋 Using Job ID: {job_id}")
    
    # Test 3: Application Service without auth (should fail)
    test_application_service_without_auth(job_id)
    
    # Test 4: Application Service with auth
    if 'tokens' in user_data and 'access' in user_data['tokens']:
        token = user_data['tokens']['access']
        test_application_service_with_auth(token, job_id)
    else:
        print("❌ No access token available")
    
    print("=" * 50)
    print("🏁 Test suite completed!")

if __name__ == "__main__":
    main()
