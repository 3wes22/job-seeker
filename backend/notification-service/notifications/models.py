from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationTemplate(models.Model):
    """
    Templates for notifications (email, SMS, push notifications).
    """
    
    name = models.CharField(max_length=100, unique=True, help_text=_("Template name"))
    subject = models.CharField(max_length=255, blank=True, help_text=_("Email subject (for email notifications)"))
    body = models.TextField(help_text=_("Notification body content"))
    
    NOTIFICATION_TYPE_CHOICES = [
        ('email', _('Email')),
        ('push', _('Push Notification')),
        ('sms', _('SMS')),
        ('in_app', _('In-App Notification')),
    ]
    
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES, help_text=_("Type of notification"))
    is_active = models.BooleanField(default=True, help_text=_("Whether the template is active"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Notification Template')
        verbose_name_plural = _('Notification Templates')
        db_table = 'notification_templates'
    
    def __str__(self):
        return f"{self.name} - {self.notification_type}"


class Notification(models.Model):
    """
    Individual notifications sent to users.
    """
    
    user_id = models.BigIntegerField(help_text=_("User ID from user-service"))
    title = models.CharField(max_length=255, help_text=_("Notification title"))
    message = models.TextField(help_text=_("Notification message"))
    
    NOTIFICATION_TYPE_CHOICES = [
        ('email', _('Email')),
        ('push', _('Push Notification')),
        ('sms', _('SMS')),
        ('in_app', _('In-App Notification')),
    ]
    
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES, help_text=_("Type of notification"))
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('sent', _('Sent')),
        ('failed', _('Failed')),
        ('read', _('Read')),
    ]
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending', help_text=_("Notification status"))
    metadata = models.JSONField(default=dict, blank=True, help_text=_("Additional metadata for the notification"))
    
    # Timestamps
    sent_at = models.DateTimeField(blank=True, null=True, help_text=_("When the notification was sent"))
    read_at = models.DateTimeField(blank=True, null=True, help_text=_("When the notification was read"))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id', 'status']),
            models.Index(fields=['notification_type', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Notification to User {self.user_id}: {self.title}"


class UserNotificationPreference(models.Model):
    """
    User preferences for notification types.
    """
    
    user_id = models.BigIntegerField(help_text=_("User ID from user-service"))
    notification_type = models.CharField(max_length=50, choices=Notification.NOTIFICATION_TYPE_CHOICES, help_text=_("Type of notification"))
    is_enabled = models.BooleanField(default=True, help_text=_("Whether this notification type is enabled for the user"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User Notification Preference')
        verbose_name_plural = _('User Notification Preferences')
        db_table = 'user_notification_preferences'
        unique_together = ('user_id', 'notification_type')
        indexes = [
            models.Index(fields=['user_id', 'is_enabled']),
        ]
    
    def __str__(self):
        return f"User {self.user_id} - {self.notification_type}: {'Enabled' if self.is_enabled else 'Disabled'}" 