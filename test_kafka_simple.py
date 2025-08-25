#!/usr/bin/env python3
"""
Simple Kafka topic creation test
"""

import logging
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    print("Starting simple Kafka topic creation test...")
    
    try:
        # Create admin client
        print("Creating Kafka admin client...")
        admin_client = KafkaAdminClient(
            bootstrap_servers=['localhost:9092'],
            client_id='test-admin'
        )
        print("Admin client created successfully")
        
        # List existing topics
        print("Listing existing topics...")
        existing_topics = admin_client.list_topics()
        print(f"Existing topics: {existing_topics}")
        
        # Create a simple test topic
        print("Creating test topic...")
        new_topic = NewTopic(
            name='test-topic',
            num_partitions=1,
            replication_factor=1
        )
        
        admin_client.create_topics([new_topic])
        print("Test topic created successfully!")
        
        # List topics again
        print("Listing topics after creation...")
        updated_topics = admin_client.list_topics()
        print(f"Updated topics: {updated_topics}")
        
        # Clean up
        admin_client.close()
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
