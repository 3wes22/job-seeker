import logging
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)

# Track changes for update events
user_original_data = {}

def get_user_event_publisher():
    """Lazy import to avoid circular import issues"""
    from .events import user_event_publisher
    return user_event_publisher

@receiver(pre_save, sender=User)
def capture_user_changes(sender, instance, **kwargs):
    """Capture original user data before save to detect changes"""
    if instance.pk:
        try:
            original = User.objects.get(pk=instance.pk)
            user_original_data[instance.pk] = {
                'username': original.username,
                'email': original.email,
                'first_name': original.first_name,
                'last_name': original.last_name,
                'user_type': original.user_type,
            }
        except User.DoesNotExist:
            pass

@receiver(post_save, sender=User)
def user_saved_handler(sender, instance, created, **kwargs):
    """Handle user creation and updates"""
    try:
        user_event_publisher = get_user_event_publisher()
        if created:
            logger.info(f"User created: {instance.username} (ID: {instance.id})")
            user_event_publisher.publish_user_created(instance)
        else:
            original_data = user_original_data.get(instance.pk, {})
            if original_data:
                changes = {}
                current_data = {
                    'username': instance.username,
                    'email': instance.email,
                    'first_name': instance.first_name,
                    'last_name': instance.last_name,
                    'user_type': instance.user_type,
                }
                for field, new_value in current_data.items():
                    old_value = original_data.get(field)
                    if old_value != new_value:
                        changes[field] = {'old': old_value, 'new': new_value}
                if changes:
                    logger.info(f"User updated: {instance.username} (ID: {instance.id})")
                    user_event_publisher.publish_user_updated(instance, changes)
                user_original_data.pop(instance.pk, None)
    except Exception as e:
        logger.error(f"Error in user_saved_handler: {str(e)}")

@receiver(post_delete, sender=User)
def user_deleted_handler(sender, instance, **kwargs):
    """Handle user deletion"""
    try:
        user_event_publisher = get_user_event_publisher()
        logger.info(f"User deleted: {instance.username} (ID: {instance.id})")
        user_event_publisher.publish_user_deleted(instance.id, instance.username)
    except Exception as e:
        logger.error(f"Error in user_deleted_handler: {str(e)}") 