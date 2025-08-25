#!/usr/bin/env python3
"""
Simple test to publish a job event and see if it gets consumed
"""

import json
from kafka import KafkaProducer
import uuid
from datetime import datetime

def main():
    print("Testing job event publishing to trigger user-service consumer...")
    
    # Create producer
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda k: k.encode('utf-8') if k else None
    )
    
    # Create a test job event
    job_event = {
        'event_id': str(uuid.uuid4()),
        'event_type': 'job_created',
        'timestamp': datetime.now().isoformat(),
        'service_name': 'test-script',
        'data': {
            'job_id': 123,
            'title': 'Test Software Engineer',
            'company_id': 456,
            'employer_id': 789,
            'employment_type': 'full_time',
            'location': 'San Francisco, CA',
            'is_remote': True,
            'salary_min': 80000.0,
            'salary_max': 120000.0
        }
    }
    
    # Publish to job-events topic
    print(f"Publishing job_created event to job-events topic...")
    future = producer.send('job-events', key='123', value=job_event)
    
    # Wait for the send to complete
    record_metadata = future.get(timeout=10)
    print(f"Event published successfully to topic: {record_metadata.topic}")
    print(f"Partition: {record_metadata.partition}")
    print(f"Offset: {record_metadata.offset}")
    
    producer.close()
    print("Test completed!")

if __name__ == "__main__":
    main()
