from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification


@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    """
    Signal to send notification when a new notification is created.
    """
    if created and instance.status == 'pending':
        # This would typically involve sending the notification
        # via email, SMS, push notification, etc.
        # For now, we'll just mark it as sent
        # Note: We need to use update to avoid triggering the signal again
        Notification.objects.filter(id=instance.id).update(status='sent') 