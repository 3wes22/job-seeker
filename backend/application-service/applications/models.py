from django.db import models
from django.utils.translation import gettext_lazy as _


class Application(models.Model):
    """
    Job application model.
    This is the core model for the application service.
    """
    
    # Foreign key references (to other services)
    job_id = models.BigIntegerField(help_text=_("Job ID from job-service"))
    applicant_id = models.BigIntegerField(help_text=_("User ID of the applicant (from user-service)"))
    employer_id = models.BigIntegerField(help_text=_("User ID of the employer (from user-service)"))
    
    # Application details
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('reviewing', _('Under Review')),
        ('shortlisted', _('Shortlisted')),
        ('interviewing', _('Interviewing')),
        ('offered', _('Offer Made')),
        ('hired', _('Hired')),
        ('rejected', _('Rejected')),
        ('withdrawn', _('Withdrawn')),
    ]
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending', help_text=_("Application status"))
    cover_letter = models.TextField(blank=True, help_text=_("Cover letter"))
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text=_("Expected salary"))
    availability_date = models.DateField(blank=True, null=True, help_text=_("Availability date"))
    
    # Status
    is_active = models.BooleanField(default=True, help_text=_("Whether the application is active"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Application')
        verbose_name_plural = _('Applications')
        db_table = 'applications'
        ordering = ['-created_at']
        unique_together = ('job_id', 'applicant_id')  # One application per job per applicant
    
    def __str__(self):
        return f"Application {self.id} - Job {self.job_id} by User {self.applicant_id}"


class ApplicationAttachment(models.Model):
    """
    Attachments for job applications (resume, cover letter, etc.).
    """
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='attachments', help_text=_("Related application"))
    file_name = models.CharField(max_length=255, help_text=_("Original file name"))
    file_path = models.CharField(max_length=500, help_text=_("File path in storage"))
    file_type = models.CharField(max_length=100, blank=True, help_text=_("File MIME type"))
    file_size = models.IntegerField(blank=True, null=True, help_text=_("File size in bytes"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Application Attachment')
        verbose_name_plural = _('Application Attachments')
        db_table = 'application_attachments'
    
    def __str__(self):
        return f"{self.file_name} - {self.application}"


class ApplicationStatusHistory(models.Model):
    """
    History of application status changes for audit trail.
    """
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='status_history', help_text=_("Related application"))
    status = models.CharField(max_length=50, help_text=_("Status at this point"))
    notes = models.TextField(blank=True, help_text=_("Notes about the status change"))
    changed_by = models.BigIntegerField(help_text=_("User ID who made the change (from user-service)"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Application Status History')
        verbose_name_plural = _('Application Status Histories')
        db_table = 'application_status_history'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.application} - {self.status} at {self.created_at}"


class Interview(models.Model):
    """
    Interview scheduling and management.
    """
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interviews', help_text=_("Related application"))
    
    INTERVIEW_TYPE_CHOICES = [
        ('phone', _('Phone Interview')),
        ('video', _('Video Interview')),
        ('in_person', _('In-Person Interview')),
    ]
    
    interview_type = models.CharField(max_length=50, choices=INTERVIEW_TYPE_CHOICES, default='phone', help_text=_("Type of interview"))
    scheduled_at = models.DateTimeField(blank=True, null=True, help_text=_("Scheduled interview time"))
    duration_minutes = models.IntegerField(default=60, help_text=_("Interview duration in minutes"))
    location = models.CharField(max_length=255, blank=True, help_text=_("Interview location or meeting link"))
    notes = models.TextField(blank=True, help_text=_("Interview notes"))
    
    STATUS_CHOICES = [
        ('scheduled', _('Scheduled')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
        ('rescheduled', _('Rescheduled')),
    ]
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='scheduled', help_text=_("Interview status"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Interview')
        verbose_name_plural = _('Interviews')
        db_table = 'interviews'
        ordering = ['-scheduled_at']
    
    def __str__(self):
        return f"Interview for {self.application} - {self.interview_type} on {self.scheduled_at}" 