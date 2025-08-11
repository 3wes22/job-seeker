from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Company(models.Model):
    """
    Company model for job postings.
    This is owned by the job service and contains company information.
    """
    
    name = models.CharField(max_length=255, help_text=_("Company name"))
    description = models.TextField(blank=True, help_text=_("Company description"))
    website = models.URLField(blank=True, help_text=_("Company website"))
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True, help_text=_("Company logo"))
    industry = models.CharField(max_length=100, blank=True, help_text=_("Company industry"))
    
    SIZE_CHOICES = [
        ('startup', _('Startup')),
        ('small', _('Small (1-50 employees)')),
        ('medium', _('Medium (51-200 employees)')),
        ('large', _('Large (200+ employees)')),
    ]
    
    size = models.CharField(max_length=50, choices=SIZE_CHOICES, blank=True, help_text=_("Company size"))
    founded_year = models.IntegerField(blank=True, null=True, help_text=_("Year company was founded"))
    location = models.CharField(max_length=255, blank=True, help_text=_("Company location"))
    is_verified = models.BooleanField(default=False, help_text=_("Whether the company is verified"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
        db_table = 'companies'
    
    def __str__(self):
        return self.name


class JobCategory(models.Model):
    """
    Job categories for organizing jobs.
    """
    
    name = models.CharField(max_length=100, unique=True, help_text=_("Category name"))
    description = models.TextField(blank=True, help_text=_("Category description"))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, help_text=_("Parent category"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Job Category')
        verbose_name_plural = _('Job Categories')
        db_table = 'job_categories'
    
    def __str__(self):
        return self.name


class JobSkill(models.Model):
    """
    Skills that can be associated with jobs.
    """
    
    name = models.CharField(max_length=100, unique=True, help_text=_("Skill name"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Job Skill')
        verbose_name_plural = _('Job Skills')
        db_table = 'job_skills'
    
    def __str__(self):
        return self.name


class Job(models.Model):
    """
    Job posting model.
    This is the core model for the job service.
    """
    
    title = models.CharField(max_length=255, help_text=_("Job title"))
    description = models.TextField(help_text=_("Job description"))
    requirements = models.TextField(blank=True, help_text=_("Job requirements"))
    responsibilities = models.TextField(blank=True, help_text=_("Job responsibilities"))
    
    # Foreign keys
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs', help_text=_("Company posting the job"))
    employer_id = models.BigIntegerField(help_text=_("User ID of the employer (from user-service)"))
    
    # Job details
    JOB_TYPE_CHOICES = [
        ('full_time', _('Full Time')),
        ('part_time', _('Part Time')),
        ('contract', _('Contract')),
        ('internship', _('Internship')),
        ('freelance', _('Freelance')),
    ]
    
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default='full_time', help_text=_("Type of job"))
    
    EXPERIENCE_LEVEL_CHOICES = [
        ('entry', _('Entry Level')),
        ('mid', _('Mid Level')),
        ('senior', _('Senior Level')),
        ('executive', _('Executive Level')),
    ]
    
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_LEVEL_CHOICES, default='entry', help_text=_("Experience level required"))
    
    # Salary information
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text=_("Minimum salary"))
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text=_("Maximum salary"))
    salary_currency = models.CharField(max_length=3, default='USD', help_text=_("Salary currency"))
    
    # Location and remote work
    location = models.CharField(max_length=255, blank=True, help_text=_("Job location"))
    is_remote = models.BooleanField(default=False, help_text=_("Whether the job is remote"))
    
    # Status and dates
    is_active = models.BooleanField(default=True, help_text=_("Whether the job posting is active"))
    application_deadline = models.DateField(blank=True, null=True, help_text=_("Application deadline"))
    
    # Many-to-many relationships
    categories = models.ManyToManyField(JobCategory, through='JobCategoryJob', related_name='jobs', help_text=_("Job categories"))
    skills = models.ManyToManyField(JobSkill, through='JobSkillJob', related_name='jobs', help_text=_("Job skills"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')
        db_table = 'jobs'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def salary_range(self):
        """Return formatted salary range."""
        if self.salary_min and self.salary_max:
            return f"{self.salary_currency} {self.salary_min:,.0f} - {self.salary_max:,.0f}"
        elif self.salary_min:
            return f"{self.salary_currency} {self.salary_min:,.0f}+"
        elif self.salary_max:
            return f"Up to {self.salary_currency} {self.salary_max:,.0f}"
        return "Salary not specified"


class JobCategoryJob(models.Model):
    """
    Through model for Job-Category many-to-many relationship.
    """
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'job_categories_jobs'
        unique_together = ('job', 'category')
    
    def __str__(self):
        return f"{self.job.title} - {self.category.name}"


class JobSkillJob(models.Model):
    """
    Through model for Job-Skill many-to-many relationship.
    """
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    skill = models.ForeignKey(JobSkill, on_delete=models.CASCADE)
    is_required = models.BooleanField(default=False, help_text=_("Whether this skill is required"))
    
    class Meta:
        db_table = 'job_skills_jobs'
        unique_together = ('job', 'skill')
    
    def __str__(self):
        return f"{self.job.title} - {self.skill.name}"


class UserProfileCache(models.Model):
    """
    Cache user data from User Service to avoid frequent API calls
    This maintains referential integrity while preserving service isolation
    """
    user_id = models.BigIntegerField(unique=True, db_index=True)
    username = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    full_name = models.CharField(max_length=300, blank=True)
    user_type = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    last_synced = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_profile_cache'
        indexes = [
            models.Index(fields=['user_type', 'is_active']),
            models.Index(fields=['last_synced']),
        ]
    
    def __str__(self):
        return f"{self.username} (ID: {self.user_id})"
    
    @property
    def is_stale(self, max_age_hours=24):
        """Check if cached data is stale"""
        from datetime import timedelta
        max_age = timezone.now() - timedelta(hours=max_age_hours)
        return self.last_synced < max_age

# Extend Job with helpers without altering existing fields
def _job_get_employer_info(self):
    try:
        return UserProfileCache.objects.get(user_id=self.employer_id)
    except UserProfileCache.DoesNotExist:
        return None

@property
def _job_employer_name(self):
    employer = self.get_employer_info()
    return employer.full_name if employer else f"User {self.employer_id}"

# Bind helper methods to Job
Job.get_employer_info = _job_get_employer_info
Job.employer_name = _job_employer_name 