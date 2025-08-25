#!/usr/bin/env python3
"""
Working Kafka Topic Setup Script for Job Platform

This script creates all the required Kafka topics for the microservices architecture.
"""

import argparse
import logging
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Topic configurations
TOPICS_CONFIG = {
    'user-events': {
        'num_partitions': 3,
        'replication_factor': 1,
        'config': {
            'retention.ms': 604800000,  # 7 days
            'cleanup.policy': 'delete',
            'compression.type': 'snappy'
        }
    },
    'job-events': {
        'num_partitions': 3,
        'replication_factor': 1,
        'config': {
            'retention.ms': 604800000,  # 7 days
            'cleanup.policy': 'delete',
            'compression.type': 'snappy'
        }
    },
    'application-events': {
        'num_partitions': 2,
        'replication_factor': 1,
        'config': {
            'retention.ms': 2592000000,  # 30 days
            'cleanup.policy': 'delete',
            'compression.type': 'snappy'
        }
    },
    'notification-events': {
        'num_partitions': 2,
        'replication_factor': 1,
        'config': {
            'retention.ms': 86400000,  # 1 day
            'cleanup.policy': 'delete',
            'compression.type': 'snappy'
        }
    },
    'search-events': {
        'num_partitions': 2,
        'replication_factor': 1,
        'config': {
            'retention.ms': 604800000,  # 7 days
            'cleanup.policy': 'delete',
            'compression.type': 'snappy'
        }
    },
    'analytics-events': {
        'num_partitions': 4,
        'replication_factor': 1,
        'config': {
            'retention.ms': 2592000000,  # 30 days
            'cleanup.policy': 'delete',
            'compression.type': 'snappy'
        }
    }
}

def test_kafka_connection(bootstrap_servers):
    """Test Kafka connection by trying to create a producer"""
    try:
        from kafka import KafkaProducer
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: str(v).encode('utf-8')
        )
        logger.info("Kafka connection test successful!")
        producer.close()
        return True
    except Exception as e:
        logger.error(f"Kafka connection test failed: {e}")
        return False

def create_topics(bootstrap_servers, topics_config):
    """Create Kafka topics"""
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers,
            client_id='topic-setup-script'
        )
        
        # Prepare topic configurations
        new_topics = []
        for topic_name, config in topics_config.items():
            topic = NewTopic(
                name=topic_name,
                num_partitions=config['num_partitions'],
                replication_factor=config['replication_factor'],
                topic_configs=config['config']
            )
            new_topics.append(topic)
        
        # Create topics
        logger.info(f"Creating {len(new_topics)} topics...")
        admin_client.create_topics(new_topics)
        
        logger.info("All topics created successfully!")
        
        # List created topics
        existing_topics = admin_client.list_topics()
        logger.info(f"Available topics: {sorted(existing_topics)}")
        
    except TopicAlreadyExistsError as e:
        logger.warning(f"Some topics already exist: {e}")
        # List existing topics
        existing_topics = admin_client.list_topics()
        logger.info(f"Available topics: {sorted(existing_topics)}")
        
    except Exception as e:
        logger.error(f"Failed to create topics: {e}")
        raise
    finally:
        admin_client.close()

def main():
    parser = argparse.ArgumentParser(description='Setup Kafka topics for Job Platform')
    parser.add_argument(
        '--bootstrap-servers',
        default='localhost:9092',
        help='Kafka bootstrap servers (default: localhost:9092)'
    )
    parser.add_argument(
        '--test-only',
        action='store_true',
        help='Only test Kafka connection without creating topics'
    )
    
    args = parser.parse_args()
    
    bootstrap_servers = args.bootstrap_servers.split(',')
    
    logger.info(f"Connecting to Kafka at: {bootstrap_servers}")
    
    # Test connection first
    if not test_kafka_connection(bootstrap_servers):
        logger.error("Cannot connect to Kafka. Please ensure Kafka is running.")
        return
    
    if args.test_only:
        logger.info("Connection test successful. Exiting.")
        return
    
    # Create topics
    try:
        create_topics(bootstrap_servers, TOPICS_CONFIG)
        logger.info("Kafka topic setup completed successfully!")
        
    except Exception as e:
        logger.error(f"Topic setup failed: {e}")
        return

if __name__ == '__main__':
    main()
