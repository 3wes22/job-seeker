from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Job, Company


@receiver(post_save, sender=Job)
def update_job_search_index(sender, instance, created, **kwargs):
    """
    Signal to update search index when a job is created or updated.
    """
    if created:
        # This would typically involve updating the search index
        # for the job in the search service
        pass


@receiver(post_save, sender=Company)
def update_company_search_index(sender, instance, created, **kwargs):
    """
    Signal to update search index when a company is created or updated.
    """
    if created:
        # This would typically involve updating the search index
        # for the company in the search service
        pass 