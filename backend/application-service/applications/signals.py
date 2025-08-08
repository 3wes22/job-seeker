from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application, ApplicationStatusHistory


@receiver(post_save, sender=Application)
def create_application_status_history(sender, instance, created, **kwargs):
    """
    Signal to create status history when application status changes.
    """
    if created:
        # Create initial status history entry
        ApplicationStatusHistory.objects.create(
            application=instance,
            status=instance.status,
            changed_by=instance.applicant_id,  # Default to applicant
            notes="Application created"
        )
    else:
        # For now, we'll create a history entry on every save
        # In production, you might want to use django-model-utils or similar
        # to track field changes more efficiently
        ApplicationStatusHistory.objects.create(
            application=instance,
            status=instance.status,
            changed_by=instance.applicant_id,  # This should be updated with actual user ID
            notes=f"Application updated"
        ) 