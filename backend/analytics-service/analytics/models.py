from django.db import models
from django.utils.translation import gettext_lazy as _


class AnalyticsEvent(models.Model):
    """
    Analytics events for tracking user behavior and system events.
    """
    
    event_type = models.CharField(max_length=100, help_text=_("Type of event"))
    user_id = models.BigIntegerField(blank=True, null=True, help_text=_("User ID from user-service (nullable for anonymous events)"))
    session_id = models.CharField(max_length=255, blank=True, help_text=_("Session identifier"))
    properties = models.JSONField(default=dict, blank=True, help_text=_("Event properties and metadata"))
    timestamp = models.DateTimeField(auto_now_add=True, help_text=_("Event timestamp"))
    
    class Meta:
        verbose_name = _('Analytics Event')
        verbose_name_plural = _('Analytics Events')
        db_table = 'analytics_events'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['event_type', 'timestamp']),
            models.Index(fields=['user_id', 'timestamp']),
            models.Index(fields=['session_id', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.event_type} - User {self.user_id or 'Anonymous'} at {self.timestamp}"


class UserAnalytics(models.Model):
    """
    User-specific analytics and metrics.
    """
    
    user_id = models.BigIntegerField(help_text=_("User ID from user-service"))
    metric_name = models.CharField(max_length=100, help_text=_("Name of the metric"))
    metric_value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, help_text=_("Metric value"))
    metric_date = models.DateField(help_text=_("Date for the metric"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('User Analytics')
        verbose_name_plural = _('User Analytics')
        db_table = 'user_analytics'
        unique_together = ('user_id', 'metric_name', 'metric_date')
        ordering = ['-metric_date', 'metric_name']
        indexes = [
            models.Index(fields=['user_id', 'metric_date']),
            models.Index(fields=['metric_name', 'metric_date']),
        ]
    
    def __str__(self):
        return f"User {self.user_id} - {self.metric_name}: {self.metric_value} on {self.metric_date}"


class JobAnalytics(models.Model):
    """
    Job-specific analytics and metrics.
    """
    
    job_id = models.BigIntegerField(help_text=_("Job ID from job-service"))
    metric_name = models.CharField(max_length=100, help_text=_("Name of the metric"))
    metric_value = models.IntegerField(default=0, help_text=_("Metric value"))
    metric_date = models.DateField(help_text=_("Date for the metric"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Job Analytics')
        verbose_name_plural = _('Job Analytics')
        db_table = 'job_analytics'
        unique_together = ('job_id', 'metric_name', 'metric_date')
        ordering = ['-metric_date', 'metric_name']
        indexes = [
            models.Index(fields=['job_id', 'metric_date']),
            models.Index(fields=['metric_name', 'metric_date']),
        ]
    
    def __str__(self):
        return f"Job {self.job_id} - {self.metric_name}: {self.metric_value} on {self.metric_date}"


class PlatformAnalytics(models.Model):
    """
    Platform-wide analytics and metrics.
    """
    
    metric_name = models.CharField(max_length=100, help_text=_("Name of the metric"))
    metric_value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, help_text=_("Metric value"))
    metric_date = models.DateField(help_text=_("Date for the metric"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Platform Analytics')
        verbose_name_plural = _('Platform Analytics')
        db_table = 'platform_analytics'
        unique_together = ('metric_name', 'metric_date')
        ordering = ['-metric_date', 'metric_name']
        indexes = [
            models.Index(fields=['metric_name', 'metric_date']),
        ]
    
    def __str__(self):
        return f"Platform - {self.metric_name}: {self.metric_value} on {self.metric_date}" 