import json
import logging
from typing import Dict, Any, Callable, Optional
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import threading
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class KafkaEventPublisher:
    """Kafka event publisher for microservices"""
    
    def __init__(self, bootstrap_servers=None):
        if bootstrap_servers is None:
            # Default fallback
            bootstrap_servers = ['localhost:9092']
            
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda v: str(v).encode('utf-8') if v else None,
            acks='all',  # Wait for all replicas
            retries=3,
            max_in_flight_requests_per_connection=1  # Ensure ordering
        )
    
    def publish_event(self, topic: str, event_type: str, data: Dict[Any, Any], 
                     key: Optional[str] = None, service_name: str = None):
        """
        Publish an event to Kafka topic
        
        Args:
            topic: Kafka topic name
            event_type: Type of event (user_created, job_created, etc.)
            data: Event data payload
            key: Optional partition key
            service_name: Name of the publishing service
        """
        event_payload = {
            'event_id': str(uuid.uuid4()),
            'event_type': event_type,
            'service_name': service_name or 'unknown',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0',
            'data': data
        }
        
        try:
            future = self.producer.send(topic, value=event_payload, key=key)
            record_metadata = future.get(timeout=10)
            
            logger.info(f"Event published successfully: {event_type} to {topic}")
            logger.debug(f"Event metadata: partition={record_metadata.partition}, offset={record_metadata.offset}")
            
        except KafkaError as e:
            logger.error(f"Failed to publish event {event_type}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error publishing event: {str(e)}")
            raise
    
    def close(self):
        """Close the producer"""
        self.producer.flush()
        self.producer.close()

class KafkaEventConsumer:
    """Kafka event consumer for microservices"""
    
    def __init__(self, topics: list, group_id: str, bootstrap_servers=None):
        if bootstrap_servers is None:
            # Default fallback
            bootstrap_servers = ['localhost:9092']
            
        self.topics = topics
        self.group_id = group_id
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda m: m.decode('utf-8') if m else None,
            auto_offset_reset='earliest',
            enable_auto_commit=False,  # Manual commit for better control
            max_poll_records=10  # Process in small batches
        )
        self.event_handlers: Dict[str, Callable] = {}
        self.is_running = False
        
    def register_handler(self, event_type: str, handler: Callable):
        """Register an event handler for a specific event type"""
        self.event_handlers[event_type] = handler
        logger.info(f"Registered handler for event type: {event_type}")
    
    def start_consuming(self):
        """Start consuming events in a separate thread"""
        if self.is_running:
            logger.warning("Consumer is already running")
            return
            
        self.is_running = True
        consumer_thread = threading.Thread(target=self._consume_events, daemon=True)
        consumer_thread.start()
        logger.info(f"Started Kafka consumer for topics: {self.topics}")
    
    def _consume_events(self):
        """Internal method to consume events"""
        try:
            for message in self.consumer:
                if not self.is_running:
                    break
                    
                try:
                    event = message.value
                    event_type = event.get('event_type')
                    
                    logger.info(f"Received event: {event_type} from topic: {message.topic}")
                    
                    # Check for duplicate processing
                    if self._is_duplicate_event(event):
                        logger.warning(f"Duplicate event detected: {event.get('event_id')}")
                        self.consumer.commit()
                        continue
                    
                    # Handle the event
                    if event_type in self.event_handlers:
                        try:
                            self.event_handlers[event_type](event)
                            self.consumer.commit()  # Commit only after successful processing
                            logger.info(f"Successfully processed event: {event_type}")
                            
                        except Exception as handler_error:
                            logger.error(f"Error processing event {event_type}: {str(handler_error)}")
                            # Could implement dead letter queue here
                            
                    else:
                        logger.warning(f"No handler registered for event type: {event_type}")
                        self.consumer.commit()  # Still commit to avoid reprocessing
                        
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Consumer error: {str(e)}")
        finally:
            self.consumer.close()
    
    def _is_duplicate_event(self, event: Dict) -> bool:
        """
        Check if this event has already been processed
        This is a simple implementation - in production, use Redis or database
        """
        # TODO: Implement proper duplicate detection
        # Could use Redis to store processed event IDs with TTL
        return False
    
    def stop_consuming(self):
        """Stop the consumer"""
        self.is_running = False
        self.consumer.close()
        logger.info("Kafka consumer stopped")

# Global instances (initialized in Django apps)
event_publisher = None
event_consumer = None

def get_event_publisher(bootstrap_servers=None) -> KafkaEventPublisher:
    """Get global event publisher instance"""
    global event_publisher
    if event_publisher is None:
        event_publisher = KafkaEventPublisher(bootstrap_servers)
    return event_publisher

def get_event_consumer(topics: list, group_id: str, bootstrap_servers=None) -> KafkaEventConsumer:
    """Get event consumer instance"""
    return KafkaEventConsumer(topics, group_id, bootstrap_servers)