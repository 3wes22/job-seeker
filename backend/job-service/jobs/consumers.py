import logging
import json
from django.conf import settings
from shared.kafka_utils import get_event_consumer
from django.db import transaction

logger = logging.getLogger(__name__)

class JobServiceEventConsumer:
    """Consumer for handling events relevant to the job service"""
    
    def __init__(self):
        self.consumer = get_event_consumer(
            topics=[settings.KAFKA_TOPICS['USER_EVENTS']],
            group_id=settings.KAFKA_GROUP_ID,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
        )
        self._register_handlers()
    
    def _register_handlers(self):
        """Register event handlers for different event types"""
        self.consumer.register_handler('user_created', self._handle_user_created)
        self.consumer.register_handler('user_updated', self._handle_user_updated)
        self.consumer.register_handler('user_deleted', self._handle_user_deleted)
        
        # Register for other relevant events
        self.consumer.register_handler('job_application_received', self._handle_job_application_received)
        self.consumer.register_handler('company_created', self._handle_company_created)
        self.consumer.register_handler('company_updated', self._handle_company_updated)
    
    def start_consuming(self):
        """Start consuming events"""
        try:
            logger.info("Starting Job Service Kafka consumer...")
            self.consumer.start_consuming()
        except Exception as e:
            logger.error(f"Failed to start Kafka consumer: {str(e)}")
            raise
    
    def stop_consuming(self):
        """Stop consuming events"""
        try:
            logger.info("Stopping Job Service Kafka consumer...")
            self.consumer.stop_consuming()
        except Exception as e:
            logger.error(f"Error stopping Kafka consumer: {str(e)}")
    
    def _handle_user_created(self, event):
        """Handle user created event"""
        try:
            user_data = event.get('data', {})
            user_id = user_data.get('user_id')
            user_type = user_data.get('user_type')
            
            logger.info(f"Handling user_created event for user {user_id} (type: {user_type})")
            
            # If it's an employer, we might want to create a default company profile
            if user_type == 'employer':
                self._create_default_company_for_employer(user_data)
            
            # Update any cached user data in the job service
            self._update_user_cache(user_data)
            
        except Exception as e:
            logger.error(f"Error handling user_created event: {str(e)}")
    
    def _handle_user_updated(self, event):
        """Handle user updated event"""
        try:
            user_data = event.get('data', {})
            user_id = user_data.get('user_id')
            changes = user_data.get('changes', {})
            
            logger.info(f"Handling user_updated event for user {user_id}")
            
            # Handle specific changes that affect jobs
            if 'user_type' in changes:
                self._handle_user_type_change(user_data, changes['user_type'])
            
            # Update cached user data
            self._update_user_cache(user_data)
            
        except Exception as e:
            logger.error(f"Error handling user_updated event: {str(e)}")
    
    def _handle_user_deleted(self, event):
        """Handle user deleted event"""
        try:
            user_data = event.get('data', {})
            user_id = user_data.get('user_id')
            
            logger.info(f"Handling user_deleted event for user {user_id}")
            
            # Handle user deletion - this might involve:
            # 1. Deactivating jobs posted by this user
            # 2. Removing user from any job applications
            # 3. Cleaning up cached data
            
            with transaction.atomic():
                # Deactivate all jobs posted by this user
                from .models import Job
                jobs_to_deactivate = Job.objects.filter(employer_id=user_id, is_active=True)
                jobs_to_deactivate.update(is_active=False, status='closed')
                
                logger.info(f"Deactivated {jobs_to_deactivate.count()} jobs for deleted user {user_id}")
            
        except Exception as e:
            logger.error(f"Error handling user_deleted event: {str(e)}")
    
    def _handle_job_application_received(self, event):
        """Handle job application received event"""
        try:
            job_data = event.get('data', {})
            job_id = job_data.get('job_id')
            application_count = job_data.get('application_count')
            
            logger.info(f"Handling job_application_received event for job {job_id}")
            
            # This event might come from the application service
            # We could update job statistics or trigger notifications
            
        except Exception as e:
            logger.error(f"Error handling job_application_received event: {str(e)}")
    
    def _handle_company_created(self, event):
        """Handle company created event"""
        try:
            company_data = event.get('data', {})
            company_id = company_data.get('company_id')
            
            logger.info(f"Handling company_created event for company {company_id}")
            
            # Update company cache or trigger related actions
            
        except Exception as e:
            logger.error(f"Error handling company_created event: {str(e)}")
    
    def _handle_company_updated(self, event):
        """Handle company updated event"""
        try:
            company_data = event.get('data', {})
            company_id = company_data.get('company_id')
            
            logger.info(f"Handling company_updated event for company {company_id}")
            
            # Update company cache or trigger related actions
            
        except Exception as e:
            logger.error(f"Error handling company_updated event: {str(e)}")
    
    def _create_default_company_for_employer(self, user_data):
        """Create a default company profile for a new employer"""
        try:
            from .models import Company
            from django.contrib.auth.models import User
            
            user_id = user_data.get('user_id')
            username = user_data.get('username')
            
            # Check if company already exists
            if not Company.objects.filter(user_id=user_id).exists():
                company = Company.objects.create(
                    user_id=user_id,
                    name=f"{username}'s Company",
                    description="Default company profile - please update with company details"
                )
                logger.info(f"Created default company profile for employer {user_id}")
            
        except Exception as e:
            logger.error(f"Error creating default company for employer: {str(e)}")
    
    def _handle_user_type_change(self, user_data, type_change):
        """Handle user type change (e.g., from job_seeker to employer)"""
        try:
            user_id = user_data.get('user_id')
            old_type = type_change.get('old')
            new_type = type_change.get('new')
            
            logger.info(f"User {user_id} type changed from {old_type} to {new_type}")
            
            if new_type == 'employer' and old_type == 'job_seeker':
                # User became an employer - create company profile if needed
                self._create_default_company_for_employer(user_data)
            elif new_type == 'job_seeker' and old_type == 'employer':
                # User became a job seeker - handle any employer-specific cleanup
                pass
                
        except Exception as e:
            logger.error(f"Error handling user type change: {str(e)}")
    
    def _update_user_cache(self, user_data):
        """Update cached user data in the job service"""
        try:
            # This could involve updating Redis cache or other caching mechanisms
            # For now, we'll just log the update
            user_id = user_data.get('user_id')
            logger.debug(f"Updated user cache for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error updating user cache: {str(e)}")

# Global consumer instance
job_service_consumer = JobServiceEventConsumer()
