from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to handle user creation.
    This can be used to create related profiles or perform other actions
    when a new user is created.
    """
    if created:
        # You can add logic here to create related objects
        # For example, create a user profile, send welcome email, etc.
        pass


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to handle user updates.
    This can be used to update related objects when a user is updated.
    """
    # You can add logic here to update related objects
    pass 