from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AnalyticsEvent


@receiver(post_save, sender=AnalyticsEvent)
def process_analytics_event(sender, instance, created, **kwargs):
    """
    Signal to process analytics events when they are created.
    """
    if created:
        # This would typically involve processing the analytics event
        # and updating relevant metrics
        pass 