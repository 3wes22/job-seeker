import logging
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Job, Company

logger = logging.getLogger(__name__)

# Track changes for update events
job_original_data = {}

def get_job_event_publisher():
    """Lazy import to avoid circular import issues"""
    from .events import job_event_publisher
    return job_event_publisher

@receiver(pre_save, sender=Job)
def capture_job_changes(sender, instance, **kwargs):
    """Capture original job data before save to detect changes"""
    if instance.pk:
        try:
            original = Job.objects.get(pk=instance.pk)
            job_original_data[instance.pk] = {
                'title': original.title,
                'description': original.description,
                'status': original.status,
                'is_active': original.is_active,
                'location': original.location,
                'is_remote': original.is_remote,
                'salary_min': original.salary_min,
                'salary_max': original.salary_max,
                'job_type': original.job_type,
                'experience_level': original.experience_level,
            }
        except Job.DoesNotExist:
            pass

@receiver(post_save, sender=Job)
def job_saved_handler(sender, instance, created, **kwargs):
    """Handle job creation and updates"""
    try:
        job_event_publisher = get_job_event_publisher()
        
        if created:
            logger.info(f"Job created: {instance.title} (ID: {instance.id})")
            job_event_publisher.publish_job_created(instance)
        else:
            original_data = job_original_data.get(instance.pk, {})
            if original_data:
                changes = {}
                current_data = {
                    'title': instance.title,
                    'description': instance.description,
                    'status': instance.status,
                    'is_active': instance.is_active,
                    'location': instance.location,
                    'is_remote': instance.is_remote,
                    'salary_min': instance.salary_min,
                    'salary_max': instance.salary_max,
                    'job_type': instance.job_type,
                    'experience_level': instance.experience_level,
                }
                
                # Check for status changes specifically
                if original_data.get('status') != instance.status:
                    old_status = original_data.get('status')
                    new_status = instance.status
                    job_event_publisher.publish_job_status_changed(instance, old_status, new_status)
                
                # Check for other field changes
                for field, new_value in current_data.items():
                    old_value = original_data.get(field)
                    if old_value != new_value:
                        changes[field] = {'old': old_value, 'new': new_value}
                
                if changes:
                    logger.info(f"Job updated: {instance.title} (ID: {instance.id})")
                    job_event_publisher.publish_job_updated(instance, changes)
                
                job_original_data.pop(instance.pk, None)
                
    except Exception as e:
        logger.error(f"Error in job_saved_handler: {str(e)}")

@receiver(post_delete, sender=Job)
def job_deleted_handler(sender, instance, **kwargs):
    """Handle job deletion"""
    try:
        job_event_publisher = get_job_event_publisher()
        logger.info(f"Job deleted: {instance.title} (ID: {instance.id})")
        job_event_publisher.publish_job_deleted(instance.id, instance.employer_id)
    except Exception as e:
        logger.error(f"Error in job_deleted_handler: {str(e)}")

@receiver(post_save, sender=Company)
def company_saved_handler(sender, instance, created, **kwargs):
    """Handle company creation and updates"""
    try:
        if created:
            logger.info(f"Company created: {instance.name} (ID: {instance.id})")
            # Could publish company events here if needed
        else:
            logger.info(f"Company updated: {instance.name} (ID: {instance.id})")
            # Could publish company update events here if needed
    except Exception as e:
        logger.error(f"Error in company_saved_handler: {str(e)}")

@receiver(post_delete, sender=Company)
def company_deleted_handler(sender, instance, **kwargs):
    """Handle company deletion"""
    try:
        logger.info(f"Company deleted: {instance.name} (ID: {instance.id})")
        # Could publish company deletion events here if needed
    except Exception as e:
        logger.error(f"Error in company_deleted_handler: {str(e)}") 