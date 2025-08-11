import logging
from django.conf import settings
from shared.kafka_utils import get_event_consumer
from .models import User

logger = logging.getLogger(__name__)

class UserEventConsumer:
    """Consumer for user service events"""
    
    def __init__(self):
        self.topics = [settings.KAFKA_TOPICS['JOB_EVENTS']]
        self.group_id = settings.KAFKA_GROUP_ID
        self.consumer = get_event_consumer(self.topics, self.group_id)
        
        # Register event handlers
        self.consumer.register_handler('job_created', self.handle_job_created)
        self.consumer.register_handler('job_updated', self.handle_job_updated)
        self.consumer.register_handler('job_deleted', self.handle_job_deleted)
    
    def handle_job_created(self, event):
        """Handle job created event"""
        try:
            data = event['data']
            job_id = data['job_id']
            employer_id = data['employer_id']
            title = data['title']
            
            logger.info(f"Received job_created event: Job {job_id} by user {employer_id}")
            
            # Example: Update user's job posting count or send notification
            # This is where you'd implement business logic based on job events
            
        except Exception as e:
            logger.error(f"Error handling job_created event: {str(e)}")
            raise  # Re-raise to trigger retry logic
    
    def handle_job_updated(self, event):
        """Handle job updated event"""
        try:
            data = event['data']
            job_id = data['job_id']
            logger.info(f"Received job_updated event: Job {job_id}")
            # Implement business logic
            
        except Exception as e:
            logger.error(f"Error handling job_updated event: {str(e)}")
            raise
    
    def handle_job_deleted(self, event):
        """Handle job deleted event"""
        try:
            data = event['data']
            job_id = data['job_id']
            logger.info(f"Received job_deleted event: Job {job_id}")
            # Implement business logic
            
        except Exception as e:
            logger.error(f"Error handling job_deleted event: {str(e)}")
            raise
    
    def start_consuming(self):
        """Start consuming events"""
        self.consumer.start_consuming()
        logger.info("User service event consumer started")

# Global instance
user_event_consumer = UserEventConsumer()