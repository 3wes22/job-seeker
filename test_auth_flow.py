#!/usr/bin/env python3
"""
Test Authentication Flow Script

This script tests the complete authentication flow to identify where the issue is occurring.
"""

import requests
import json
import time

# Configuration
USER_SERVICE_URL = "http://localhost:8001"
JOB_SERVICE_URL = "http://localhost:8002"
APPLICATION_SERVICE_URL = "http://localhost:8003"

def test_service_health():
    """Test if all services are running"""
    print("🔍 Testing service health...")
    
    services = {
        "User Service": f"{USER_SERVICE_URL}/",
        "Job Service": f"{JOB_SERVICE_URL}/",
        "Application Service": f"{APPLICATION_SERVICE_URL}/"
    }
    
    for name, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            print(f"✅ {name}: {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: {e}")

def test_user_registration():
    """Test user registration"""
    print("\n🔐 Testing user registration...")
    
    # Generate unique username and email
    timestamp = int(time.time())
    username = f"testuser_{timestamp}"
    email = f"test{timestamp}@example.com"
    
    data = {
        "username": username,
        "email": email,
        "password": "testpass123",
        "password_confirm": "testpass123",
        "user_type": "employer",
        "phone_number": "+1234567890",
        "date_of_birth": "1990-01-01"
    }
    
    try:
        response = requests.post(
            f"{USER_SERVICE_URL}/api/users/register/",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Registration successful: {result['message']}")
            print(f"   User ID: {result['user']['id']}")
            print(f"   Access Token: {result['tokens']['access'][:20]}...")
            print(f"   Refresh Token: {result['tokens']['refresh'][:20]}...")
            return result['tokens']['access'], result['user']['id']
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None, None

def test_user_login():
    """Test user login"""
    print("\n🔑 Testing user login...")
    
    data = {
        "email": "test@example.com",  # Use a known test user
        "password": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{USER_SERVICE_URL}/api/users/login/",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Login successful: {result['message']}")
            print(f"   User ID: {result['user']['id']}")
            print(f"   Access Token: {result['tokens']['access'][:20]}...")
            print(f"   Refresh Token: {result['tokens']['refresh'][:20]}...")
            return result['tokens']['access'], result['user']['id']
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None, None

def test_profile_access(token):
    """Test accessing user profile with token"""
    print("\n👤 Testing profile access...")
    
    if not token:
        print("❌ No token provided")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{USER_SERVICE_URL}/api/users/profile/",
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Profile access successful")
            print(f"   User ID: {result['id']}")
            print(f"   Email: {result['email']}")
            print(f"   User Type: {result['user_type']}")
            return True
        else:
            print(f"❌ Profile access failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Profile access error: {e}")
        return False

def test_job_creation(token, user_id):
    """Test job creation with token"""
    print("\n💼 Testing job creation...")
    
    if not token:
        print("❌ No token provided")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # First, create a company
        company_data = {
            "name": "Test Company for Job Posting",
            "description": "Test company created during testing",
            "industry": "Technology",
            "size": "medium",
            "employer_id": user_id
        }
        
        print("   Creating company...")
        company_response = requests.post(
            f"{JOB_SERVICE_URL}/api/jobs/companies/create/",
            json=company_data,
            headers=headers
        )
        
        if company_response.status_code == 201:
            company = company_response.json()
            company_id = company['id']
            print(f"   ✅ Company created: {company['name']} (ID: {company_id})")
        else:
            print(f"   ❌ Company creation failed: {company_response.status_code}")
            print(f"      Response: {company_response.text}")
            return False
        
        # Now create a job
        job_data = {
            "title": "Test Job for Authentication Testing",
            "description": "This is a test job to verify authentication is working",
            "company": company_id,
            "location": "Remote",
            "job_type": "full_time",
            "experience_level": "mid",
            "is_remote": True,
            "requirements": "Python, Django, Testing",
            "responsibilities": "Test the authentication system"
        }
        
        print("   Creating job...")
        job_response = requests.post(
            f"{JOB_SERVICE_URL}/api/jobs/create/",
            json=job_data,
            headers=headers
        )
        
        if job_response.status_code == 201:
            job = job_response.json()
            print(f"   ✅ Job created: {job['title']} (ID: {job['id']})")
            return True
        else:
            print(f"   ❌ Job creation failed: {job_response.status_code}")
            print(f"      Response: {job_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Job creation error: {e}")
        return False

def test_token_refresh(refresh_token):
    """Test token refresh"""
    print("\n🔄 Testing token refresh...")
    
    if not refresh_token:
        print("❌ No refresh token provided")
        return None
    
    try:
        data = {"refresh": refresh_token}
        
        response = requests.post(
            f"{USER_SERVICE_URL}/api/users/refresh/",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            new_access_token = result['access']
            print(f"✅ Token refresh successful")
            print(f"   New Access Token: {new_access_token[:20]}...")
            return new_access_token
        else:
            print(f"❌ Token refresh failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Token refresh error: {e}")
        return None

def main():
    """Main test function"""
    print("🧪 Testing Authentication Flow")
    print("=" * 50)
    
    # Test service health
    test_service_health()
    
    # Test user registration
    access_token, user_id = test_user_registration()
    
    if not access_token:
        # Try login instead
        print("\n🔄 Registration failed, trying login...")
        access_token, user_id = test_user_login()
    
    if access_token and user_id:
        # Test profile access
        profile_success = test_profile_access(access_token)
        
        if profile_success:
            # Test job creation
            job_success = test_job_creation(access_token, user_id)
            
            if job_success:
                print("\n🎉 All authentication tests passed!")
            else:
                print("\n❌ Job creation failed - this is the issue!")
        else:
            print("\n❌ Profile access failed - authentication issue!")
    else:
        print("\n❌ No valid tokens obtained - authentication failed!")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    main()
