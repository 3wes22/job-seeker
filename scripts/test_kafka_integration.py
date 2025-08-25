#!/usr/bin/env python3
"""
Kafka Integration Test Script for Job Platform

This script tests the Kafka integration between microservices by:
1. Publishing test events
2. Verifying event consumption
3. Testing event flow between services
"""

import argparse
import logging
import time
import json
import sys
import os
from datetime import datetime
from threading import Thread, Event

# Add the shared directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend', 'shared'))

from kafka_utils import get_event_publisher, get_event_consumer
from events import UserCreatedEvent, JobCreatedEvent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class KafkaIntegrationTester:
    """Test Kafka integration between services"""
    
    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers
        self.test_results = {}
        self.stop_event = Event()
        
        # Test event data
        self.test_user_data = {
            'user_id': 999,
            'username': 'test_user',
            'email': 'test@example.com',
            'user_type': 'employer',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        self.test_job_data = {
            'job_id': 999,
            'title': 'Test Job Position',
            'company_id': 999,
            'employer_id': 999,
            'job_type': 'full_time',
            'location': 'Test City',
            'is_remote': False,
            'salary_min': 50000.0,
            'salary_max': 80000.0
        }
    
    def test_user_service_events(self):
        """Test user service event publishing"""
        logger.info("Testing User Service Event Publishing...")
        
        try:
            publisher = get_event_publisher(self.bootstrap_servers)
            
            # Test user created event
            user_event = UserCreatedEvent(
                event_id='test-user-created-001',
                timestamp=datetime.now().isoformat(),
                service_name='test-service',
                **self.test_user_data
            )
            
            publisher.publish_event(
                topic='user-events',
                event_type='user_created',
                data=user_event.to_dict(),
                key=str(self.test_user_data['user_id']),
                service_name='test-service'
            )
            
            logger.info("✓ User created event published successfully")
            self.test_results['user_service_publishing'] = True
            
            # Test user updated event
            user_updated_event = UserCreatedEvent(
                event_id='test-user-updated-001',
                timestamp=datetime.now().isoformat(),
                service_name='test-service',
                **self.test_user_data
            )
            
            publisher.publish_event(
                topic='user-events',
                event_type='user_updated',
                data=user_updated_event.to_dict(),
                key=str(self.test_user_data['user_id']),
                service_name='test-service'
            )
            
            logger.info("✓ User updated event published successfully")
            self.test_results['user_service_publishing'] = True
            
            publisher.close()
            
        except Exception as e:
            logger.error(f"✗ User service event publishing failed: {e}")
            self.test_results['user_service_publishing'] = False
    
    def test_job_service_events(self):
        """Test job service event publishing"""
        logger.info("Testing Job Service Event Publishing...")
        
        try:
            publisher = get_event_publisher(self.bootstrap_servers)
            
            # Test job created event
            job_event = JobCreatedEvent(
                event_id='test-job-created-001',
                timestamp=datetime.now().isoformat(),
                service_name='test-service',
                **self.test_job_data
            )
            
            publisher.publish_event(
                topic='job-events',
                event_type='job_created',
                data=job_event.to_dict(),
                key=str(self.test_job_data['job_id']),
                service_name='test-service'
            )
            
            logger.info("✓ Job created event published successfully")
            self.test_results['job_service_publishing'] = True
            
            # Test job status changed event
            job_status_data = {
                'job_id': self.test_job_data['job_id'],
                'title': self.test_job_data['title'],
                'company_id': self.test_job_data['company_id'],
                'employer_id': self.test_job_data['employer_id'],
                'old_status': 'draft',
                'new_status': 'active',
                'status_changed_at': datetime.now().isoformat()
            }
            
            publisher.publish_event(
                topic='job-events',
                event_type='job_status_changed',
                data=job_status_data,
                key=str(self.test_job_data['job_id']),
                service_name='test-service'
            )
            
            logger.info("✓ Job status changed event published successfully")
            self.test_results['job_service_publishing'] = True
            
            publisher.close()
            
        except Exception as e:
            logger.error(f"✗ Job service event publishing failed: {e}")
            self.test_results['job_service_publishing'] = False
    
    def test_event_consumption(self):
        """Test event consumption from both topics"""
        logger.info("Testing Event Consumption...")
        
        try:
            # Test user events consumption
            user_consumer = get_event_consumer(
                topics=['user-events'],
                group_id='test-consumer-group',
                bootstrap_servers=self.bootstrap_servers
            )
            
            # Test job events consumption
            job_consumer = get_event_consumer(
                topics=['job-events'],
                group_id='test-consumer-group',
                bootstrap_servers=self.bootstrap_servers
            )
            
            logger.info("✓ Event consumers created successfully")
            self.test_results['event_consumption'] = True
            
            # Clean up
            user_consumer.stop_consuming()
            job_consumer.stop_consuming()
            
        except Exception as e:
            logger.error(f"✗ Event consumption test failed: {e}")
            self.test_results['event_consumption'] = False
    
    def test_cross_service_events(self):
        """Test events that flow between services"""
        logger.info("Testing Cross-Service Event Flow...")
        
        try:
            publisher = get_event_publisher(self.bootstrap_servers)
            
            # Test job application received event (from application service to job service)
            application_event = {
                'job_id': self.test_job_data['job_id'],
                'title': self.test_job_data['title'],
                'company_id': self.test_job_data['company_id'],
                'employer_id': self.test_job_data['employer_id'],
                'application_count': 1,
                'max_applications': 10,
                'received_at': datetime.now().isoformat()
            }
            
            publisher.publish_event(
                topic='job-events',
                event_type='job_application_received',
                data=application_event,
                key=str(self.test_job_data['job_id']),
                service_name='test-service'
            )
            
            logger.info("✓ Cross-service event published successfully")
            self.test_results['cross_service_events'] = True
            
            publisher.close()
            
        except Exception as e:
            logger.error(f"✗ Cross-service event test failed: {e}")
            self.test_results['cross_service_events'] = False
    
    def run_all_tests(self):
        """Run all integration tests"""
        logger.info("Starting Kafka Integration Tests...")
        logger.info("=" * 50)
        
        # Test 1: User Service Events
        self.test_user_service_events()
        time.sleep(1)
        
        # Test 2: Job Service Events
        self.test_job_service_events()
        time.sleep(1)
        
        # Test 3: Event Consumption
        self.test_event_consumption()
        time.sleep(1)
        
        # Test 4: Cross-Service Events
        self.test_cross_service_events()
        time.sleep(1)
        
        # Print results
        self.print_test_results()
    
    def print_test_results(self):
        """Print test results summary"""
        logger.info("=" * 50)
        logger.info("KAFKA INTEGRATION TEST RESULTS")
        logger.info("=" * 50)
        
        all_passed = True
        for test_name, result in self.test_results.items():
            status = "✓ PASS" if result else "✗ FAIL"
            logger.info(f"{test_name}: {status}")
            if not result:
                all_passed = False
        
        logger.info("=" * 50)
        if all_passed:
            logger.info("🎉 ALL TESTS PASSED! Kafka integration is working correctly.")
        else:
            logger.error("❌ SOME TESTS FAILED. Please check the logs above.")
        
        return all_passed

def main():
    parser = argparse.ArgumentParser(description='Test Kafka integration for Job Platform')
    parser.add_argument(
        '--bootstrap-servers',
        default='localhost:9092',
        help='Kafka bootstrap servers (default: localhost:9092)'
    )
    
    args = parser.parse_args()
    bootstrap_servers = args.bootstrap_servers.split(',')
    
    logger.info(f"Testing Kafka integration with servers: {bootstrap_servers}")
    
    try:
        tester = KafkaIntegrationTester(bootstrap_servers)
        success = tester.run_all_tests()
        
        if not success:
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Integration test failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
