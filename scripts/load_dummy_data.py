#!/usr/bin/env python3
"""
Script to load dummy data into the job platform services
"""
import json
import requests
import time
import sys
import os
from typing import Dict, List, Any

class DummyDataLoader:
    """Load dummy data into backend services"""
    
    def __init__(self, base_url: str = "http://localhost"):
        self.base_url = base_url
        self.services = {
            "user": f"{base_url}:8001",
            "job": f"{base_url}:8002",
            "application": f"{base_url}:8003",
        }
        self.auth_tokens = {}
        
    def register_user(self, user_data: Dict[str, Any], service_url: str) -> bool:
        """Register a single user"""
        try:
            response = requests.post(
                f"{service_url}/api/users/register/",
                json=user_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print(f"✓ Registered user: {user_data['username']}")
                return True
            else:
                print(f"✗ Failed to register {user_data['username']}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Error registering {user_data['username']}: {e}")
            return False
    
    def create_company(self, company_data: Dict[str, Any], service_url: str, auth_token: str) -> bool:
        """Create a single company"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"}
            response = requests.post(
                f"{service_url}/api/jobs/companies/create/",
                json=company_data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print(f"✓ Created company: {company_data['name']}")
                return True
            else:
                print(f"✗ Failed to create company {company_data['name']}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Error creating company {company_data['name']}: {e}")
            return False
    
    def create_job_category(self, category_data: Dict[str, Any], service_url: str) -> bool:
        """Create a job category"""
        try:
            response = requests.post(
                f"{service_url}/api/jobs/categories/create/",
                json=category_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print(f"✓ Created category: {category_data['name']}")
                return True
            else:
                print(f"✗ Failed to create category {category_data['name']}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Error creating category {category_data['name']}: {e}")
            return False
    
    def create_job_skill(self, skill_data: Dict[str, Any], service_url: str) -> bool:
        """Create a job skill"""
        try:
            response = requests.post(
                f"{service_url}/api/jobs/skills/create/",
                json=skill_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print(f"✓ Created skill: {skill_data['name']}")
                return True
            else:
                print(f"✗ Failed to create skill {skill_data['name']}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Error creating skill {skill_data['name']}: {e}")
            return False
    
    def create_job(self, job_data: Dict[str, Any], service_url: str, auth_token: str) -> bool:
        """Create a single job"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"}
            response = requests.post(
                f"{service_url}/api/jobs/create/",
                json=job_data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print(f"✓ Created job: {job_data['title']}")
                return True
            else:
                print(f"✗ Failed to create job {job_data['title']}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Error creating job {job_data['title']}: {e}")
            return False
    
    def get_auth_token(self, username: str, password: str, service_url: str) -> str:
        """Get authentication token for a user"""
        try:
            response = requests.post(
                f"{service_url}/api/users/login/",
                json={"email": f"{username}@example.com", "password": password},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'tokens' in data:
                    return data['tokens']['access']
                elif 'access' in data:
                    return data['access']
            
            return ""
            
        except Exception as e:
            print(f"✗ Error getting auth token for {username}: {e}")
            return ""
    
    def wait_for_services(self) -> bool:
        """Wait for all services to be available"""
        print("Waiting for services to be available...")
        
        for service_name, service_url in self.services.items():
            max_retries = 30
            for i in range(max_retries):
                try:
                    response = requests.get(f"{service_url}/health/", timeout=5)
                    if response.status_code == 200:
                        print(f"✓ {service_name} service is ready")
                        break
                except:
                    if i == max_retries - 1:
                        print(f"✗ {service_name} service not available after {max_retries} retries")
                        return False
                    print(f"  Waiting for {service_name} service... ({i+1}/{max_retries})")
                    time.sleep(2)
        
        return True
    
    def load_data_from_files(self, data_dir: str = "backend/shared/dummy_data") -> Dict[str, List[Dict[str, Any]]]:
        """Load dummy data from JSON files"""
        data = {}
        
        files = [
            "users.json", "companies.json", "job_categories.json", 
            "job_skills.json", "jobs.json", "applications.json"
        ]
        
        for filename in files:
            filepath = os.path.join(data_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    key = filename.replace('.json', '')
                    data[key] = json.load(f)
                print(f"✓ Loaded {len(data[key])} {key}")
            else:
                print(f"✗ File not found: {filepath}")
        
        return data
    
    def load_all_data(self):
        """Load all dummy data into services"""
        print("Starting dummy data loading process...")
        
        # Wait for services
        if not self.wait_for_services():
            print("✗ Services not available. Exiting.")
            return False
        
        # Generate dummy data if files don't exist
        data_dir = "backend/shared/dummy_data"
        if not os.path.exists(data_dir):
            print("Generating dummy data...")
            sys.path.append('backend/shared')
            from dummy_data import DummyDataGenerator
            generator = DummyDataGenerator()
            generator.save_to_files(data_dir)
        
        # Load data from files
        data = self.load_data_from_files(data_dir)
        
        if not data:
            print("✗ No data to load. Exiting.")
            return False
        
        # Load users first
        print("\n📊 Loading users...")
        user_service = self.services["user"]
        job_service = self.services["job"]
        
        success_count = 0
        for user in data.get("users", []):
            if self.register_user(user, user_service):
                success_count += 1
        
        print(f"✓ Loaded {success_count}/{len(data.get('users', []))} users")
        
        # Get auth token for an employer user
        print("\n🔐 Getting authentication token...")
        employer_users = [u for u in data.get("users", []) if u.get("user_type") == "employer"]
        if employer_users:
            employer = employer_users[0]
            auth_token = self.get_auth_token(employer["username"], employer["password"], user_service)
            if auth_token:
                print(f"✓ Got auth token for {employer['username']}")
            else:
                print("✗ Failed to get auth token")
                return False
        else:
            print("✗ No employer users found")
            return False
        
        # Load job categories
        print("\n📚 Loading job categories...")
        success_count = 0
        for category in data.get("job_categories", []):
            if self.create_job_category(category, job_service):
                success_count += 1
        
        print(f"✓ Loaded {success_count}/{len(data.get('job_categories', []))} categories")
        
        # Load job skills
        print("\n🛠️  Loading job skills...")
        success_count = 0
        for skill in data.get("job_skills", []):
            if self.create_job_skill(skill, job_service):
                success_count += 1
        
        print(f"✓ Loaded {success_count}/{len(data.get('job_skills', []))} skills")
        
        # Load companies
        print("\n🏢 Loading companies...")
        success_count = 0
        for company in data.get("companies", []):
            if self.create_company(company, job_service, auth_token):
                success_count += 1
        
        print(f"✓ Loaded {success_count}/{len(data.get('companies', []))} companies")
        
        # Load jobs
        print("\n💼 Loading jobs...")
        success_count = 0
        for job in data.get("jobs", []):
            if self.create_job(job, job_service, auth_token):
                success_count += 1
        
        print(f"✓ Loaded {success_count}/{len(data.get('jobs', []))} jobs")
        
        print("\n🎉 Dummy data loading completed!")
        return True

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Load dummy data into job platform services")
    parser.add_argument("--base-url", default="http://localhost", help="Base URL for services")
    parser.add_argument("--generate-only", action="store_true", help="Only generate data files, don't load")
    
    args = parser.parse_args()
    
    if args.generate_only:
        sys.path.append('backend/shared')
        from dummy_data import DummyDataGenerator
        generator = DummyDataGenerator()
        generator.save_to_files()
        print("✓ Dummy data files generated!")
    else:
        loader = DummyDataLoader(args.base_url)
        success = loader.load_all_data()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
