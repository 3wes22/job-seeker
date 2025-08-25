import logging
from django.conf import settings
from shared.kafka_utils import get_event_publisher
from shared.events import JobCreatedEvent, JobUpdatedEvent, JobDeletedEvent
import uuid
from django.utils import timezone

logger = logging.getLogger(__name__)

class JobEventPublisher:
    """Publisher for job-related events"""
    
    def __init__(self):
        self.publisher = get_event_publisher(settings.KAFKA_BOOTSTRAP_SERVERS)
        self.topic = settings.KAFKA_TOPICS['JOB_EVENTS']
        self.service_name = 'job-service'
    
    def publish_job_created(self, job):
        """Publish job created event"""
        try:
            event = JobCreatedEvent(
                event_id=str(uuid.uuid4()),
                timestamp=timezone.now().isoformat(),
                service_name=self.service_name,
                job_id=job.id,
                title=job.title,
                company_id=job.company.id,
                employer_id=job.employer.id,
                job_type=job.employment_type,
                location=job.location,
                is_remote=job.is_remote,
                salary_min=float(job.salary_min) if job.salary_min else None,
                salary_max=float(job.salary_max) if job.salary_max else None
            )
            
            self.publisher.publish_event(
                topic=self.topic,
                event_type='job_created',
                data=event.to_dict(),
                key=str(job.id),
                service_name=self.service_name
            )
            
            logger.info(f"Published job_created event for job {job.id}")
            
        except Exception as e:
            logger.error(f"Failed to publish job_created event: {str(e)}")
            # Don't raise - we don't want to fail job creation due to event failure
    
    def publish_job_updated(self, job, changes=None):
        """Publish job updated event"""
        try:
            event = JobUpdatedEvent(
                event_id=str(uuid.uuid4()),
                timestamp=timezone.now().isoformat(),
                service_name=self.service_name,
                job_id=job.id,
                title=job.title,
                company_id=job.company.id,
                employer_id=job.employer.id,
                changes=changes or {}
            )
            
            self.publisher.publish_event(
                topic=self.topic,
                event_type='job_updated',
                data=event.to_dict(),
                key=str(job.id),
                service_name=self.service_name
            )
            
            logger.info(f"Published job_updated event for job {job.id}")
            
        except Exception as e:
            logger.error(f"Failed to publish job_updated event: {str(e)}")
    
    def publish_job_deleted(self, job_id, employer_id):
        """Publish job deleted event"""
        try:
            event = JobDeletedEvent(
                event_id=str(uuid.uuid4()),
                timestamp=timezone.now().isoformat(),
                service_name=self.service_name,
                job_id=job_id,
                employer_id=employer_id
            )
            
            self.publisher.publish_event(
                topic=self.topic,
                event_type='job_deleted',
                data=event.to_dict(),
                key=str(job_id),
                service_name=self.service_name
            )
            
            logger.info(f"Published job_deleted event for job {job_id}")
            
        except Exception as e:
            logger.error(f"Failed to publish job_deleted event: {str(e)}")
    
    def publish_job_status_changed(self, job, old_status, new_status):
        """Publish job status change event"""
        try:
            event_data = {
                'job_id': job.id,
                'title': job.title,
                'company_id': job.company.id,
                'employer_id': job.employer.id,
                'old_status': old_status,
                'new_status': new_status,
                'status_changed_at': timezone.now().isoformat()
            }
            
            self.publisher.publish_event(
                topic=self.topic,
                event_type='job_status_changed',
                data=event_data,
                key=str(job.id),
                service_name=self.service_name
            )
            
            logger.info(f"Published job_status_changed event for job {job.id}: {old_status} -> {new_status}")
            
        except Exception as e:
            logger.error(f"Failed to publish job_status_changed event: {str(e)}")
    
    def publish_job_application_received(self, job, application_count):
        """Publish job application received event"""
        try:
            event_data = {
                'job_id': job.id,
                'title': job.title,
                'company_id': job.company.id,
                'employer_id': job.employer.id,
                'application_count': application_count,
                'max_applications': job.max_applications,
                'received_at': timezone.now().isoformat()
            }
            
            self.publisher.publish_event(
                topic=self.topic,
                event_type='job_application_received',
                data=event_data,
                key=str(job.id),
                service_name=self.service_name
            )
            
            logger.info(f"Published job_application_received event for job {job.id}")
            
        except Exception as e:
            logger.error(f"Failed to publish job_application_received event: {str(e)}")

# Global instance
job_event_publisher = JobEventPublisher()
