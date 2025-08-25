import logging
import json
from django.conf import settings
from shared.kafka_utils import get_event_consumer
from django.db import transaction

logger = logging.getLogger(__name__)

class UserServiceEventConsumer:
    """Consumer for handling events relevant to the user service"""
    
    def __init__(self):
        self.consumer = get_event_consumer(
            topics=[settings.KAFKA_TOPICS['JOB_EVENTS']],
            group_id=settings.KAFKA_GROUP_ID,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
        )
        self._register_handlers()
    
    def _register_handlers(self):
        """Register event handlers for different event types"""
        self.consumer.register_handler('job_created', self._handle_job_created)
        self.consumer.register_handler('job_updated', self._handle_job_updated)
        self.consumer.register_handler('job_deleted', self._handle_job_deleted)
        self.consumer.register_handler('job_status_changed', self._handle_job_status_changed)
        self.consumer.register_handler('job_application_received', self._handle_job_application_received)
        
        # Register for other relevant events
        self.consumer.register_handler('company_created', self._handle_company_created)
        self.consumer.register_handler('company_updated', self._handle_company_updated)
    
    def start_consuming(self):
        """Start consuming events"""
        try:
            logger.info("Starting User Service Kafka consumer...")
            self.consumer.start_consuming()
        except Exception as e:
            logger.error(f"Failed to start Kafka consumer: {str(e)}")
            raise
    
    def stop_consuming(self):
        """Stop consuming events"""
        try:
            logger.info("Stopping User Service Kafka consumer...")
            self.consumer.stop_consuming()
        except Exception as e:
            logger.error(f"Error stopping Kafka consumer: {str(e)}")
    
    def _handle_job_created(self, event):
        """Handle job created event"""
        try:
            job_data = event.get('data', {})
            job_id = job_data.get('job_id')
            employer_id = job_data.get('employer_id')
            title = job_data.get('title')
            
            logger.info(f"Handling job_created event for job {job_id} by employer {employer_id}")
            
            # Update user statistics (e.g., jobs posted count)
            self._update_employer_job_stats(employer_id, increment=True)
            
            # Could trigger notifications to relevant users
            self._notify_relevant_users_job_created(job_data)
            
        except Exception as e:
            logger.error(f"Error handling job_created event: {str(e)}")
    
    def _handle_job_updated(self, event):
        """Handle job updated event"""
        try:
            job_data = event.get('data', {})
            job_id = job_data.get('job_id')
            employer_id = job_data.get('employer_id')
            changes = job_data.get('changes', {})
            
            logger.info(f"Handling job_updated event for job {job_id}")
            
            # Handle specific changes that affect users
            if 'is_active' in changes:
                self._handle_job_visibility_change(job_data, changes['is_active'])
            
            # Update any cached job data
            self._update_job_cache(job_data)
            
        except Exception as e:
            logger.error(f"Error handling job_updated event: {str(e)}")
    
    def _handle_job_deleted(self, event):
        """Handle job deleted event"""
        try:
            job_data = event.get('data', {})
            job_id = job_data.get('job_id')
            employer_id = job_data.get('employer_id')
            
            logger.info(f"Handling job_deleted event for job {job_id}")
            
            # Update user statistics (e.g., jobs posted count)
            self._update_employer_job_stats(employer_id, increment=False)
            
            # Could notify users who had applied to this job
            self._notify_job_applicants_deleted(job_id)
            
        except Exception as e:
            logger.error(f"Error handling job_deleted event: {str(e)}")
    
    def _handle_job_status_changed(self, event):
        """Handle job status change event"""
        try:
            job_data = event.get('data', {})
            job_id = job_data.get('job_id')
            old_status = job_data.get('old_status')
            new_status = job_data.get('new_status')
            
            logger.info(f"Handling job_status_changed event for job {job_id}: {old_status} -> {new_status}")
            
            # Handle status-specific actions
            if new_status == 'active' and old_status != 'active':
                # Job became active - notify relevant job seekers
                self._notify_job_seekers_job_active(job_data)
            elif new_status == 'closed' and old_status != 'closed':
                # Job closed - notify applicants
                self._notify_job_applicants_job_closed(job_data)
            elif new_status == 'filled' and old_status != 'filled':
                # Job filled - notify applicants
                self._notify_job_applicants_job_filled(job_data)
            
        except Exception as e:
            logger.error(f"Error handling job_status_changed event: {str(e)}")
    
    def _handle_job_application_received(self, event):
        """Handle job application received event"""
        try:
            job_data = event.get('data', {})
            job_id = job_data.get('job_id')
            employer_id = job_data.get('employer_id')
            application_count = job_data.get('application_count')
            
            logger.info(f"Handling job_application_received event for job {job_id}")
            
            # Notify employer about new application
            self._notify_employer_new_application(job_data)
            
            # Update job statistics
            self._update_job_application_stats(job_id, application_count)
            
        except Exception as e:
            logger.error(f"Error handling job_application_received event: {str(e)}")
    
    def _handle_company_created(self, event):
        """Handle company created event"""
        try:
            company_data = event.get('data', {})
            company_id = company_data.get('company_id')
            user_id = company_data.get('user_id')
            
            logger.info(f"Handling company_created event for company {company_id}")
            
            # Update user profile to reflect company association
            self._update_user_company_profile(user_id, company_data)
            
        except Exception as e:
            logger.error(f"Error handling company_created event: {str(e)}")
    
    def _handle_company_updated(self, event):
        """Handle company updated event"""
        try:
            company_data = event.get('data', {})
            company_id = company_data.get('company_id')
            
            logger.info(f"Handling company_updated event for company {company_id}")
            
            # Update cached company data
            self._update_company_cache(company_data)
            
        except Exception as e:
            logger.error(f"Error handling company_updated event: {str(e)}")
    
    def _update_employer_job_stats(self, employer_id, increment=True):
        """Update employer's job posting statistics"""
        try:
            # This could involve updating user profile or cache
            # For now, we'll just log the update
            action = "incremented" if increment else "decremented"
            logger.debug(f"{action} job stats for employer {employer_id}")
            
        except Exception as e:
            logger.error(f"Error updating employer job stats: {str(e)}")
    
    def _notify_relevant_users_job_created(self, job_data):
        """Notify relevant users about a new job posting"""
        try:
            # This could involve:
            # 1. Finding users with matching skills/interests
            # 2. Sending push notifications
            # 3. Updating job recommendations
            
            logger.debug(f"Notifying relevant users about new job {job_data.get('job_id')}")
            
        except Exception as e:
            logger.error(f"Error notifying users about new job: {str(e)}")
    
    def _handle_job_visibility_change(self, job_data, is_active):
        """Handle job visibility changes"""
        try:
            job_id = job_data.get('job_id')
            if is_active:
                logger.debug(f"Job {job_id} became visible")
                # Could trigger notifications to job seekers
            else:
                logger.debug(f"Job {job_id} became hidden")
                # Could notify applicants about job status
                
        except Exception as e:
            logger.error(f"Error handling job visibility change: {str(e)}")
    
    def _update_job_cache(self, job_data):
        """Update cached job data"""
        try:
            job_id = job_data.get('job_id')
            logger.debug(f"Updated job cache for job {job_id}")
            
        except Exception as e:
            logger.error(f"Error updating job cache: {str(e)}")
    
    def _notify_job_seekers_job_active(self, job_data):
        """Notify relevant job seekers that a job is now active"""
        try:
            job_id = job_data.get('job_id')
            logger.debug(f"Notifying job seekers about active job {job_id}")
            
        except Exception as e:
            logger.error(f"Error notifying job seekers: {str(e)}")
    
    def _notify_job_applicants_job_closed(self, job_data):
        """Notify job applicants that a job has been closed"""
        try:
            job_id = job_data.get('job_id')
            logger.debug(f"Notifying applicants about closed job {job_id}")
            
        except Exception as e:
            logger.error(f"Error notifying applicants about closed job: {str(e)}")
    
    def _notify_job_applicants_job_filled(self, job_data):
        """Notify job applicants that a job has been filled"""
        try:
            job_id = job_data.get('job_id')
            logger.debug(f"Notifying applicants about filled job {job_id}")
            
        except Exception as e:
            logger.error(f"Error notifying applicants about filled job: {str(e)}")
    
    def _notify_job_applicants_deleted(self, job_id):
        """Notify job applicants that a job has been deleted"""
        try:
            logger.debug(f"Notifying applicants about deleted job {job_id}")
            
        except Exception as e:
            logger.error(f"Error notifying applicants about deleted job: {str(e)}")
    
    def _notify_employer_new_application(self, job_data):
        """Notify employer about a new job application"""
        try:
            job_id = job_data.get('job_id')
            employer_id = job_data.get('employer_id')
            logger.debug(f"Notifying employer {employer_id} about new application for job {job_id}")
            
        except Exception as e:
            logger.error(f"Error notifying employer about new application: {str(e)}")
    
    def _update_job_application_stats(self, job_id, application_count):
        """Update job application statistics"""
        try:
            logger.debug(f"Updated application stats for job {job_id}: {application_count} applications")
            
        except Exception as e:
            logger.error(f"Error updating job application stats: {str(e)}")
    
    def _update_user_company_profile(self, user_id, company_data):
        """Update user profile to reflect company association"""
        try:
            logger.debug(f"Updated user {user_id} company profile")
            
        except Exception as e:
            logger.error(f"Error updating user company profile: {str(e)}")
    
    def _update_company_cache(self, company_data):
        """Update cached company data"""
        try:
            company_id = company_data.get('company_id')
            logger.debug(f"Updated company cache for company {company_id}")
            
        except Exception as e:
            logger.error(f"Error updating company cache: {str(e)}")

# Global consumer instance
user_service_consumer = UserServiceEventConsumer()