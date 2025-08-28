#!/usr/bin/env python3
"""
Phase 1 Comprehensive Testing Script for Job Platform

This script systematically tests all working endpoints and functionality
to ensure a solid foundation before proceeding to Phase 2.
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Configuration
SERVICES = {
    'user': {'url': 'http://localhost:8001', 'port': 8001},
    'job': {'url': 'http://localhost:8002', 'port': 8002},
    'application': {'url': 'http://localhost:8003', 'port': 8003}
}

# Test data
TEST_USER_DATA = {
    'username': f'testuser_{int(time.time())}',
    'email': f'test{int(time.time())}@example.com',
    'password': 'testpass123',
    'password_confirm': 'testpass123',
    'user_type': 'job_seeker',
    'phone_number': '+1234567890',
    'date_of_birth': '1990-01-01'
}

TEST_JOB_DATA = {
    'title': 'Test Job for Phase 1 Testing',
    'description': 'This is a test job created during Phase 1 testing',
    'requirements': 'Python, Django, Testing',
    'responsibilities': 'Test the job platform functionality',
    'job_type': 'full_time',
    'experience_level': 'mid',
    'location': 'Remote',
    'is_remote': True,
    'salary_min': 60000,
    'salary_max': 80000,
    'salary_currency': 'USD',
    'company': 'Test Company',
    'employer_id': 1,
    'is_active': True
}

class Phase1Tester:
    def __init__(self):
        self.results = {
            'service_health': {},
            'api_endpoints': {},
            'authentication': {},
            'data_flow': {},
            'performance': {}
        }
        self.access_token = None
        self.refresh_token = None
        self.user_id = None
        self.job_id = None
        self.application_id = None
        
    def print_header(self, title: str):
        """Print a formatted header"""
        print(f"\n{'='*60}")
        print(f"🧪 {title}")
        print(f"{'='*60}")
        
    def print_section(self, title: str):
        """Print a formatted section header"""
        print(f"\n📋 {title}")
        print(f"{'-'*40}")
        
    def print_result(self, test_name: str, status: str, details: str = ""):
        """Print a formatted test result"""
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {status}")
        if details:
            print(f"   📝 {details}")
            
    def test_service_health(self) -> bool:
        """Test if all services are running and responding"""
        self.print_header("Phase 1: Service Health & Basic Connectivity")
        
        all_healthy = True
        
        for service_name, service_info in SERVICES.items():
            self.print_section(f"Testing {service_name.title()} Service (Port {service_info['port']})")
            
            try:
                # Test service response by checking if it's accessible
                # Django services typically return 404 for root path, which is normal
                response = requests.get(f"{service_info['url']}/", timeout=5)
                if response.status_code in [200, 404]:  # 404 is normal for Django root
                    self.print_result(f"{service_name.title()} Service Running", "PASS", 
                                   f"Responding on port {service_info['port']} (Status: {response.status_code})")
                    self.results['service_health'][service_name] = 'PASS'
                else:
                    self.print_result(f"{service_name.title()} Service Running", "FAIL", 
                                   f"Unexpected status code: {response.status_code}")
                    self.results['service_health'][service_name] = 'FAIL'
                    all_healthy = False
                    
                # Test admin access
                admin_response = requests.get(f"{service_info['url']}/admin/", timeout=5)
                if admin_response.status_code in [200, 302]:  # 302 is redirect to login
                    self.print_result(f"{service_name.title()} Admin Access", "PASS", "Admin interface accessible")
                else:
                    self.print_result(f"{service_name.title()} Admin Access", "FAIL", 
                                   f"Status code: {admin_response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                self.print_result(f"{service_name.title()} Service", "FAIL", f"Connection error: {str(e)}")
                self.results['service_health'][service_name] = 'FAIL'
                all_healthy = False
                
        return all_healthy
        
    def test_user_service_endpoints(self) -> bool:
        """Test user service API endpoints"""
        self.print_header("Phase 2: User Service API Endpoint Testing")
        
        all_passed = True
        
        # Test user registration
        self.print_section("User Registration Endpoint")
        try:
            response = requests.post(
                f"{SERVICES['user']['url']}/api/users/register/",
                json=TEST_USER_DATA,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                self.access_token = data['tokens']['access']
                self.refresh_token = data['tokens']['refresh']
                self.user_id = data['user']['id']
                
                self.print_result("User Registration", "PASS", 
                               f"User created with ID: {self.user_id}")
                self.results['api_endpoints']['user_registration'] = 'PASS'
            else:
                self.print_result("User Registration", "FAIL", 
                               f"Status: {response.status_code}, Response: {response.text}")
                self.results['api_endpoints']['user_registration'] = 'FAIL'
                all_passed = False
                
        except Exception as e:
            self.print_result("User Registration", "FAIL", f"Error: {str(e)}")
            self.results['api_endpoints']['user_registration'] = 'FAIL'
            all_passed = False
            
        # Test user login
        self.print_section("User Login Endpoint")
        try:
            login_data = {
                'email': TEST_USER_DATA['email'],
                'password': TEST_USER_DATA['password']
            }
            
            response = requests.post(
                f"{SERVICES['user']['url']}/api/users/login/",
                json=login_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data['tokens']['access']
                self.refresh_token = data['tokens']['refresh']
                
                self.print_result("User Login", "PASS", "Login successful, tokens received")
                self.results['api_endpoints']['user_login'] = 'PASS'
            else:
                self.print_result("User Login", "FAIL", 
                               f"Status: {response.status_code}, Response: {response.text}")
                self.results['api_endpoints']['user_login'] = 'FAIL'
                all_passed = False
                
        except Exception as e:
            self.print_result("User Login", "FAIL", f"Error: {str(e)}")
            self.results['api_endpoints']['user_login'] = 'FAIL'
            all_passed = False
            
        # Test profile endpoint
        if self.access_token:
            self.print_section("User Profile Endpoint")
            try:
                headers = {'Authorization': f'Bearer {self.access_token}'}
                response = requests.get(
                    f"{SERVICES['user']['url']}/api/users/profile/",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.print_result("User Profile", "PASS", "Profile retrieved successfully")
                    self.results['api_endpoints']['user_profile'] = 'PASS'
                else:
                    self.print_result("User Profile", "FAIL", 
                                   f"Status: {response.status_code}, Response: {response.text}")
                    self.results['api_endpoints']['user_profile'] = 'FAIL'
                    all_passed = False
                    
            except Exception as e:
                self.print_result("User Profile", "FAIL", f"Error: {str(e)}")
                self.results['api_endpoints']['user_profile'] = 'FAIL'
                all_passed = False
                
        return all_passed
        
    def test_job_service_endpoints(self) -> bool:
        """Test job service API endpoints"""
        self.print_header("Phase 2: Job Service API Endpoint Testing")
        
        all_passed = True
        
        # Test job listing
        self.print_section("Job List Endpoint")
        try:
            response = requests.get(
                f"{SERVICES['job']['url']}/api/jobs/",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if len(data) > 0:
                    self.job_id = data[0]['id']
                    self.print_result("Job List", "PASS", f"Retrieved {len(data)} jobs, first job ID: {self.job_id}")
                    self.results['api_endpoints']['job_list'] = 'PASS'
                else:
                    self.print_result("Job List", "WARNING", "No jobs found in database")
                    self.results['api_endpoints']['job_list'] = 'WARNING'
            else:
                self.print_result("Job List", "FAIL", 
                               f"Status: {response.status_code}, Response: {response.text}")
                self.results['api_endpoints']['job_list'] = 'FAIL'
                all_passed = False
                
        except Exception as e:
            self.print_result("Job List", "FAIL", f"Error: {str(e)}")
            self.results['api_endpoints']['job_list'] = 'FAIL'
            all_passed = False
            
        # Test job detail
        if self.job_id:
            self.print_section("Job Detail Endpoint")
            try:
                response = requests.get(
                    f"{SERVICES['job']['url']}/api/jobs/{self.job_id}/",
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.print_result("Job Detail", "PASS", f"Job details retrieved: {data['title']}")
                    self.results['api_endpoints']['job_detail'] = 'PASS'
                else:
                    self.print_result("Job Detail", "FAIL", 
                                   f"Status: {response.status_code}, Response: {response.text}")
                    self.results['api_endpoints']['job_detail'] = 'FAIL'
                    all_passed = False
                    
            except Exception as e:
                self.print_result("Job Detail", "FAIL", f"Error: {str(e)}")
                self.results['api_endpoints']['job_detail'] = 'FAIL'
                all_passed = False
                
        return all_passed
        
    def test_application_service_endpoints(self) -> bool:
        """Test application service API endpoints"""
        self.print_header("Phase 2: Application Service API Endpoint Testing")
        
        all_passed = True
        
        if not self.access_token or not self.job_id:
            self.print_result("Application Testing", "FAIL", "Missing access token or job ID")
            return False
            
        # Test application status check
        self.print_section("Application Status Check Endpoint")
        try:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            response = requests.get(
                f"{SERVICES['application']['url']}/api/applications/check-status/{self.job_id}/",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_result("Application Status Check", "PASS", 
                               f"Status: {data.get('has_applied', 'unknown')}")
                self.results['api_endpoints']['application_status_check'] = 'PASS'
            else:
                self.print_result("Application Status Check", "FAIL", 
                               f"Status: {response.status_code}, Response: {response.text}")
                self.results['api_endpoints']['application_status_check'] = 'FAIL'
                all_passed = False
                
        except Exception as e:
            self.print_result("Application Status Check", "FAIL", f"Error: {str(e)}")
            self.results['api_endpoints']['application_status_check'] = 'FAIL'
            all_passed = False
            
        # Test application creation
        self.print_section("Application Creation Endpoint")
        try:
            application_data = {
                'job_id': self.job_id,
                'employer_id': 1,
                'cover_letter': 'I am interested in this position for Phase 1 testing',
                'expected_salary': 70000,
                'availability_date': '2025-09-01'
            }
            
            response = requests.post(
                f"{SERVICES['application']['url']}/api/applications/create/",
                json=application_data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                self.application_id = data.get('application_id')
                self.print_result("Application Creation", "PASS", 
                               f"Application created with ID: {self.application_id}")
                self.results['api_endpoints']['application_creation'] = 'PASS'
            else:
                self.print_result("Application Creation", "FAIL", 
                               f"Status: {response.status_code}, Response: {response.text}")
                self.results['api_endpoints']['application_creation'] = 'FAIL'
                all_passed = False
                
        except Exception as e:
            self.print_result("Application Creation", "FAIL", f"Error: {str(e)}")
            self.results['api_endpoints']['application_creation'] = 'FAIL'
            all_passed = False
            
        # Test user applications list
        self.print_section("User Applications List Endpoint")
        try:
            response = requests.get(
                f"{SERVICES['application']['url']}/api/applications/my-applications/",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_result("User Applications List", "PASS", 
                               f"Retrieved {len(data)} applications")
                self.results['api_endpoints']['user_applications_list'] = 'PASS'
            else:
                self.print_result("User Applications List", "FAIL", 
                               f"Status: {response.status_code}, Response: {response.text}")
                self.results['api_endpoints']['user_applications_list'] = 'FAIL'
                all_passed = False
                
        except Exception as e:
            self.print_result("User Applications List", "FAIL", f"Error: {str(e)}")
            self.results['api_endpoints']['user_applications_list'] = 'FAIL'
            all_passed = False
            
        return all_passed
        
    def test_jwt_authentication(self) -> bool:
        """Test JWT authentication flow"""
        self.print_header("Phase 3: JWT Authentication Testing")
        
        all_passed = True
        
        if not self.access_token or not self.refresh_token:
            self.print_result("JWT Testing", "FAIL", "Missing access or refresh token")
            return False
            
        # Test token validation
        self.print_section("Token Validation")
        try:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            response = requests.get(
                f"{SERVICES['user']['url']}/api/users/profile/",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                self.print_result("Token Validation", "PASS", "Valid token accepted")
                self.results['authentication']['token_validation'] = 'PASS'
            else:
                self.print_result("Token Validation", "FAIL", 
                               f"Status: {response.status_code}, Response: {response.text}")
                self.results['authentication']['token_validation'] = 'FAIL'
                all_passed = False
                
        except Exception as e:
            self.print_result("Token Validation", "FAIL", f"Error: {str(e)}")
            self.results['authentication']['token_validation'] = 'FAIL'
            all_passed = False
            
        # Test token refresh
        self.print_section("Token Refresh")
        try:
            response = requests.post(
                f"{SERVICES['user']['url']}/api/users/refresh/",
                json={'refresh': self.refresh_token},
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                new_access_token = data.get('access')
                if new_access_token:
                    self.access_token = new_access_token
                    self.print_result("Token Refresh", "PASS", "New access token received")
                    self.results['authentication']['token_refresh'] = 'PASS'
                else:
                    self.print_result("Token Refresh", "FAIL", "No new access token in response")
                    self.results['authentication']['token_refresh'] = 'FAIL'
                    all_passed = False
            else:
                self.print_result("Token Refresh", "FAIL", 
                               f"Status: {response.status_code}, Response: {response.text}")
                self.results['authentication']['token_refresh'] = 'FAIL'
                all_passed = False
                
        except Exception as e:
            self.print_result("Token Refresh", "FAIL", f"Error: {str(e)}")
            self.results['authentication']['token_refresh'] = 'FAIL'
            all_passed = False
            
        # Test invalid token rejection
        self.print_section("Invalid Token Rejection")
        try:
            headers = {'Authorization': 'Bearer invalid_token'}
            response = requests.get(
                f"{SERVICES['user']['url']}/api/users/profile/",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 401:
                self.print_result("Invalid Token Rejection", "PASS", "Invalid token properly rejected")
                self.results['authentication']['invalid_token_rejection'] = 'PASS'
            else:
                self.print_result("Invalid Token Rejection", "FAIL", 
                               f"Status: {response.status_code}, should be 401")
                self.results['authentication']['invalid_token_rejection'] = 'FAIL'
                all_passed = False
                
        except Exception as e:
            self.print_result("Invalid Token Rejection", "FAIL", f"Error: {str(e)}")
            self.results['authentication']['invalid_token_rejection'] = 'FAIL'
            all_passed = False
            
        return all_passed
        
    def test_data_flow(self) -> bool:
        """Test complete data flow and consistency"""
        self.print_header("Phase 4: Data Flow Testing")
        
        all_passed = True
        
        # Test complete user journey
        self.print_section("Complete User Journey")
        journey_steps = [
            ("User Registration", "user_registration"),
            ("User Login", "user_login"), 
            ("Job Browsing", "job_list"),
            ("Job Details View", "job_detail"),
            ("Job Application", "application_creation"),
            ("Application Status Check", "application_status_check"),
            ("User Applications List", "user_applications_list")
        ]
        
        for step_name, test_key in journey_steps:
            if test_key in self.results['api_endpoints'] and self.results['api_endpoints'][test_key] == 'PASS':
                self.print_result(f"Journey Step: {step_name}", "PASS")
            else:
                self.print_result(f"Journey Step: {step_name}", "FAIL")
                all_passed = False
                
        # Test data consistency
        self.print_section("Data Consistency Checks")
        
        if self.user_id and self.job_id and self.application_id:
            self.print_result("Data Consistency", "PASS", 
                           f"User ID: {self.user_id}, Job ID: {self.job_id}, Application ID: {self.application_id}")
            self.results['data_flow']['data_consistency'] = 'PASS'
        else:
            self.print_result("Data Consistency", "FAIL", "Missing required IDs")
            self.results['data_flow']['data_consistency'] = 'FAIL'
            all_passed = False
            
        # Test token persistence across services
        if self.access_token:
            self.print_section("Token Persistence Across Services")
            
            services_to_test = ['user', 'application']
            for service in services_to_test:
                try:
                    headers = {'Authorization': f'Bearer {self.access_token}'}
                    if service == 'user':
                        response = requests.get(
                            f"{SERVICES[service]['url']}/api/users/profile/",
                            headers=headers,
                            timeout=10
                        )
                    elif service == 'application':
                        response = requests.get(
                            f"{SERVICES[service]['url']}/api/applications/my-applications/",
                            headers=headers,
                            timeout=10
                        )
                        
                    if response.status_code == 200:
                        self.print_result(f"Token Persistence - {service.title()} Service", "PASS")
                    else:
                        self.print_result(f"Token Persistence - {service.title()} Service", "FAIL")
                        all_passed = False
                        
                except Exception as e:
                    self.print_result(f"Token Persistence - {service.title()} Service", "FAIL", f"Error: {str(e)}")
                    all_passed = False
                    
        return all_passed
        
    def generate_test_report(self):
        """Generate a comprehensive test report"""
        self.print_header("Phase 1 Testing Results Summary")
        
        # Calculate overall statistics
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        warning_tests = 0
        
        for category, tests in self.results.items():
            for test_name, result in tests.items():
                total_tests += 1
                if result == 'PASS':
                    passed_tests += 1
                elif result == 'FAIL':
                    failed_tests += 0
                elif result == 'WARNING':
                    warning_tests += 1
                    
        # Print summary
        print(f"\n📊 Overall Test Results:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   ⚠️  Warnings: {warning_tests}")
        
        # Calculate success rate
        if total_tests > 0:
            success_rate = (passed_tests / total_tests) * 100
            print(f"   📈 Success Rate: {success_rate:.1f}%")
            
            if success_rate >= 90:
                print(f"   🎉 Phase 1 Status: READY FOR PHASE 2")
            elif success_rate >= 75:
                print(f"   ⚠️  Phase 1 Status: NEEDS MINOR FIXES")
            else:
                print(f"   🚨 Phase 1 Status: NEEDS MAJOR FIXES")
                
        # Print detailed results by category
        for category, tests in self.results.items():
            if tests:
                print(f"\n📋 {category.replace('_', ' ').title()}:")
                for test_name, result in tests.items():
                    status_icon = "✅" if result == "PASS" else "❌" if result == "FAIL" else "⚠️"
                    print(f"   {status_icon} {test_name}: {result}")
                    
        # Recommendations
        print(f"\n💡 Recommendations:")
        if failed_tests > 0:
            print(f"   🔧 Fix {failed_tests} failed tests before proceeding")
        if warning_tests > 0:
            print(f"   ⚠️  Address {warning_tests} warnings for better stability")
        if passed_tests == total_tests:
            print(f"   🚀 All tests passed! Ready to proceed to Phase 2")
            
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"phase1_test_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'results': self.results,
                'summary': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'failed_tests': failed_tests,
                    'warning_tests': warning_tests,
                    'success_rate': success_rate if total_tests > 0 else 0
                }
            }, f, indent=2)
            
        print(f"\n📁 Detailed results saved to: {filename}")
        
    def run_all_tests(self):
        """Run all Phase 1 tests"""
        print("🚀 Starting Phase 1 Comprehensive Testing...")
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all test phases
        tests = [
            ("Service Health", self.test_service_health),
            ("User Service Endpoints", self.test_user_service_endpoints),
            ("Job Service Endpoints", self.test_job_service_endpoints),
            ("Application Service Endpoints", self.test_application_service_endpoints),
            ("JWT Authentication", self.test_jwt_authentication),
            ("Data Flow", self.test_data_flow)
        ]
        
        all_passed = True
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                if not result:
                    all_passed = False
            except Exception as e:
                print(f"❌ Error running {test_name}: {str(e)}")
                all_passed = False
                
        # Generate final report
        self.generate_test_report()
        
        return all_passed

def main():
    """Main function to run the testing"""
    print("🧪 Job Platform - Phase 1 Comprehensive Testing")
    print("=" * 60)
    
    # Check if services are accessible
    print("🔍 Checking service accessibility...")
    for service_name, service_info in SERVICES.items():
        try:
            response = requests.get(f"{service_info['url']}/", timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name.title()} service is accessible")
            else:
                print(f"⚠️  {service_name.title()} service responded with status {response.status_code}")
        except requests.exceptions.RequestException:
            print(f"❌ {service_name.title()} service is not accessible")
            print(f"   Please ensure the service is running on port {service_info['port']}")
            
    print("\n" + "=" * 60)
    
    # Run tests
    tester = Phase1Tester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n🚨 Some tests failed. Please review and fix issues before proceeding.")
        sys.exit(1)

if __name__ == "__main__":
    main()
