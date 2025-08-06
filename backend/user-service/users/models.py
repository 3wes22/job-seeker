from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model for the job platform.
    Extends Django's AbstractUser with additional fields.
    """
    
    # Additional fields
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        help_text=_("User's phone number")
    )
    
    date_of_birth = models.DateField(
        blank=True, 
        null=True,
        help_text=_("User's date of birth")
    )
    
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True, 
        null=True,
        help_text=_("User's profile picture")
    )
    
    bio = models.TextField(
        max_length=500, 
        blank=True,
        help_text=_("User's bio/description")
    )
    
    # User type (job seeker, employer, admin)
    USER_TYPE_CHOICES = [
        ('job_seeker', _('Job Seeker')),
        ('employer', _('Employer')),
        ('admin', _('Admin')),
    ]
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='job_seeker',
        help_text=_("Type of user")
    )
    
    # Account status
    is_verified = models.BooleanField(
        default=False,
        help_text=_("Whether the user's email is verified")
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text=_("Whether the user account is active")
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'users'
    
    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip() or self.username
