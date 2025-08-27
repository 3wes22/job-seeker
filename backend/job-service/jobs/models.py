from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# =============================================================================
# JOB SERVICE MODELS - CORE ENTITIES FOR JOB POSTING AND MANAGEMENT
# =============================================================================
# This module contains all models related to job posting, including:
# - Company information for employers
# - Job categories and skills for classification
# - Job postings with detailed requirements
# - Relationships between jobs, categories, and skills
# =============================================================================

class Company(models.Model):
    """
    Company Model - Represents employer organizations posting jobs
    
    PURPOSE: Stores company information for job postings
    RELATIONSHIP: References user ID from user-service via employer_id field
    
    KEY FEATURES:
    - Company identification and branding
    - Industry and size classification
    - Location and contact information
    - Verification status for trust
    """
    

    
    # ========================================================================
    # CORE COMPANY FIELDS - Essential company information
    # ========================================================================
    
    # Company Identification
    name = models.CharField(
        max_length=200,
        help_text="Official company name for job postings"
    )
    
    # Company Details
    industry = models.CharField(
        max_length=100,
        blank=True,
        help_text="Primary industry sector (e.g., Technology, Healthcare)"
    )
    
    size = models.CharField(
        max_length=50,
        choices=[
            ('startup', 'Startup'),
            ('small', 'Small (1-50 employees)'),
            ('medium', 'Medium (51-200 employees)'),
            ('large', 'Large (200+ employees)'),
        ],
        blank=True,
        help_text="Company size classification"
    )
    
    # Location Information
    location = models.CharField(
        max_length=200,
        blank=True,
        help_text="Company location (city, state, country)"
    )
    
    # Contact Information
    website = models.URLField(
        blank=True,
        help_text="Company website URL for additional information"
    )
    
    # Company Description
    description = models.TextField(
        blank=True,
        help_text="Company description, mission, and culture"
    )
    
    # Verification Status
    is_verified = models.BooleanField(
        default=False,
        help_text="Indicates if company has been verified by platform"
    )
    
    # ========================================================================
    # RELATIONSHIPS - Links to other models
    # ========================================================================
    employer_id = models.IntegerField(
        default=1,
        help_text="ID of the user account associated with this company"
    )
    
    # ========================================================================
    # TIMESTAMP FIELDS - Audit trail for company changes
    # ========================================================================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ========================================================================
    # META CONFIGURATION - Django model settings
    # ========================================================================
    class Meta:
        db_table = 'companies'
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['-created_at']

    # ========================================================================
    # STRING REPRESENTATION - How company appears in admin and logs
    # ========================================================================
    def __str__(self):
        return f"{self.name} ({self.get_size_display()})"

    # ========================================================================
    # BUSINESS LOGIC METHODS - Company-specific operations
    # ========================================================================
    
    def get_active_jobs_count(self):
        """
        Returns the number of active job postings for this company
        
        USAGE: job_count = company.get_active_jobs_count() # show in company profile
        RETURNS: Integer count of active job postings
        """
        return self.jobs.filter(is_active=True).count()

    def get_total_jobs_count(self):
        """
        Returns the total number of job postings (active + inactive)
        
        USAGE: total_jobs = company.get_total_jobs_count() # for analytics
        RETURNS: Integer count of all job postings
        """
        return self.jobs.count()

# =============================================================================
# JOB CATEGORY MODEL - HIERARCHICAL JOB CLASSIFICATION
# =============================================================================
# This model provides a flexible, hierarchical structure for categorizing jobs.
# Categories can have parent categories, allowing for nested classifications
# like "Technology > Software Development > Frontend Development".
# =============================================================================

class JobCategory(models.Model):
    """
    Job Category Model - Hierarchical job classification system
    
    PURPOSE: Organizes jobs into logical categories for search and filtering
    FEATURES: Self-referencing parent-child relationships for nested categories
    
    EXAMPLE HIERARCHY:
    - Technology
      - Software Development
        - Frontend Development
        - Backend Development
      - Data Science
        - Machine Learning
        - Data Analysis
    """
    
    # ========================================================================
    # CORE CATEGORY FIELDS - Category identification and structure
    # ========================================================================
    
    # Category Information
    name = models.CharField(
        max_length=100,
        help_text="Category name (e.g., 'Software Development')"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Detailed description of what this category encompasses"
    )
    
    # Hierarchical Structure
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='children',
        help_text="Parent category for nested hierarchies (null for top-level)"
    )
    
    # Category Metadata
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Icon identifier for UI display (e.g., 'code', 'database')"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this category is active and visible"
    )
    
    # ========================================================================
    # TIMESTAMP FIELDS - Audit trail
    # ========================================================================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ========================================================================
    # META CONFIGURATION
    # ========================================================================
    class Meta:
        db_table = 'job_categories'
        verbose_name = 'Job Category'
        verbose_name_plural = 'Job Categories'
        ordering = ['name']
        unique_together = ['name', 'parent']  # Prevent duplicate names under same parent

    # ========================================================================
    # STRING REPRESENTATION
    # ========================================================================
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    # ========================================================================
    # BUSINESS LOGIC METHODS - Category-specific operations
    # ========================================================================
    
    def get_full_path(self):
        """
        Returns the complete category path from root to current category
        
        USAGE: path = category.get_full_path() # show breadcrumb navigation
        RETURNS: String with full category path (e.g., "Technology > Software Development")
        """
        path = [self.name]
        current = self.parent
        
        while current:
            path.append(current.name)
            current = current.parent
        
        return ' > '.join(reversed(path))

    def get_jobs_count(self):
        """
        Returns the number of jobs in this category (including subcategories)
        
        USAGE: count = category.get_jobs_count() # show category statistics
        RETURNS: Integer count of jobs in this category and all subcategories
        """
        # Count jobs directly in this category
        direct_count = self.jobs.count()
        
        # Count jobs in all subcategories recursively
        subcategory_count = sum(child.get_jobs_count() for child in self.children.all())
        
        return direct_count + subcategory_count

    def get_all_children(self):
        """
        Returns all descendant categories (children, grandchildren, etc.)
        
        USAGE: all_children = category.get_all_children() # for category management
        RETURNS: QuerySet of all descendant categories
        """
        children = list(self.children.all())
        for child in children:
            children.extend(child.get_all_children())
        return children

# =============================================================================
# JOB SKILL MODEL - SKILLS REQUIRED FOR JOBS
# =============================================================================
# This model represents individual skills that can be associated with jobs.
# Skills can be marked as required or optional, and can have proficiency levels.
# =============================================================================

class JobSkill(models.Model):
    """
    Job Skill Model - Individual skills required for job positions
    
    PURPOSE: Defines specific skills that can be associated with jobs
    FEATURES: Skill categorization, proficiency levels, and requirement status
    
    EXAMPLES: Python, JavaScript, Project Management, Communication
    """
    
    # ========================================================================
    # SKILL LEVEL CHOICES - Proficiency level classifications
    # ========================================================================
    SKILL_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    # ========================================================================
    # CORE SKILL FIELDS - Skill identification and classification
    # ========================================================================
    
    # Skill Information
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Skill name (e.g., 'Python', 'Project Management')"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the skill and its applications"
    )
    
    # Skill Classification
    category = models.CharField(
        max_length=50,
        blank=True,
        help_text="Skill category (e.g., 'Programming', 'Soft Skills')"
    )
    
    skill_level = models.CharField(
        max_length=20,
        choices=SKILL_LEVEL_CHOICES,
        blank=True,
        help_text="Default proficiency level for this skill"
    )
    
    # Skill Metadata
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Icon identifier for UI display"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this skill is active and available"
    )
    
    # ========================================================================
    # TIMESTAMP FIELDS - Audit trail
    # ========================================================================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ========================================================================
    # META CONFIGURATION
    # ========================================================================
    class Meta:
        db_table = 'job_skills'
        verbose_name = 'Job Skill'
        verbose_name_plural = 'Job Skills'
        ordering = ['name']

    # ========================================================================
    # STRING REPRESENTATION
    # ========================================================================
    def __str__(self):
        return self.name

    # ========================================================================
    # BUSINESS LOGIC METHODS - Skill-specific operations
    # ========================================================================
    
    def get_jobs_count(self):
        """
        Returns the number of jobs that require this skill
        
        USAGE: count = skill.get_jobs_count() # show skill demand
        RETURNS: Integer count of jobs requiring this skill
        """
        return self.job_skills.count()

    def get_related_skills(self):
        """
        Returns skills that are commonly used together with this skill
        
        USAGE: related = skill.get_related_skills() # suggest additional skills
        RETURNS: QuerySet of commonly co-occurring skills
        """
        # This could be enhanced with machine learning recommendations
        return JobSkill.objects.filter(category=self.category).exclude(id=self.id)[:5]

# =============================================================================
# JOB MODEL - CORE JOB POSTING ENTITY
# =============================================================================
# This is the main model for job postings. It contains all the information
# about a job position including requirements, responsibilities, and metadata.
# Jobs are linked to companies, categories, and skills through relationships.
# =============================================================================

class Job(models.Model):
    """
    Job Model - Core entity for job postings and applications
    
    PURPOSE: Stores complete information about job positions
    RELATIONSHIPS: Links to Company, Categories, Skills, and Applications
    
    KEY FEATURES:
    - Comprehensive job details and requirements
    - Salary and location information
    - Application and deadline management
    - Status tracking and visibility control
    """
    
    # ========================================================================
    # JOB STATUS CHOICES - Current state of the job posting
    # ========================================================================
    JOB_STATUS_CHOICES = [
        ('draft', 'Draft'),                 # Job is being prepared
        ('active', 'Active'),               # Job is visible and accepting applications
        ('paused', 'Paused'),               # Job is temporarily paused
        ('closed', 'Closed'),               # Job is closed, no more applications
        ('filled', 'Filled'),               # Job has been filled
        ('expired', 'Expired'),             # Job has expired
    ]
    
    # ========================================================================
    # JOB TYPE CHOICES - Type of employment arrangement
    # ========================================================================
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    ]
    
    # ========================================================================
    # EXPERIENCE LEVEL CHOICES - Required experience for the position
    # ========================================================================
    EXPERIENCE_LEVEL_CHOICES = [
        ('entry', 'Entry Level'),
        ('junior', 'Junior'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior'),
        ('lead', 'Lead'),
        ('executive', 'Executive'),
    ]
    
    # ========================================================================
    # CORE JOB FIELDS - Essential job information
    # ========================================================================
    
    # Job Identification
    title = models.CharField(
        max_length=200,
        help_text="Job title (e.g., 'Senior Software Engineer')"
    )
    
    # Job Details
    description = models.TextField(
        help_text="Detailed job description, responsibilities, and requirements"
    )
    
    requirements = models.TextField(
        blank=True,
        help_text="Specific requirements and qualifications for the position"
    )
    
    responsibilities = models.TextField(
        blank=True,
        help_text="Key responsibilities and duties for the role"
    )
    
    # Employment Information
    job_type = models.CharField(
        max_length=50,
        choices=JOB_TYPE_CHOICES,
        default='full_time',
        help_text="Type of employment arrangement"
    )
    
    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_LEVEL_CHOICES,
        default='mid',
        help_text="Required experience level for the position"
    )
    
    # Location and Remote Work
    location = models.CharField(
        max_length=200,
        help_text="Job location (city, state, country)"
    )
    
    is_remote = models.BooleanField(
        default=False,
        help_text="Whether the job allows remote work"
    )
    
    # remote_type = models.CharField(
    #     max_length=20,
    #     choices=[
    #         ('on_site', 'On Site'),
    #         ('remote', 'Remote'),
    #         ('hybrid', 'Hybrid'),
    #     ],
    #     default='on_site',
    #     help_text="Type of work arrangement"
    # )
    
    # Salary Information
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Minimum annual salary (USD)"
    )
    
    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Maximum annual salary (USD)"
    )
    
    salary_currency = models.CharField(
        max_length=3,
        default='USD',
        help_text="Salary currency code (e.g., USD, EUR, GBP)"
    )
    
    # Application Management
    # application_deadline = models.DateTimeField(
    #     blank=True,
    #     null=True,
    #     help_text="Deadline for job applications"
    # )
    
    # max_applications = models.PositiveIntegerField(
    #     blank=True,
    #     null=True,
    #     help_text="Maximum number of applications allowed"
    # )
    
    # Job Status and Visibility
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the job is visible to job seekers"
    )
    
    # is_featured = models.BooleanField(
    #     default=False,
    #     help_text="Whether the job is featured/promoted"
    # )
    
    # ========================================================================
    # RELATIONSHIPS - Links to other models
    # ========================================================================
    
    # Company and Employer
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='jobs',
        help_text="Company posting this job"
    )
    
    employer_id = models.IntegerField(
        default=1,
        help_text="ID of the user who posted this job"
    )
    
    # Categories and Skills
    categories = models.ManyToManyField(
        JobCategory,
        through='JobCategoryJob',
        related_name='jobs',
        help_text="Job categories for classification and search"
    )
    
    skills = models.ManyToManyField(
        JobSkill,
        through='JobSkillJob',
        related_name='jobs',
        help_text="Skills required for this job"
    )
    
    # ========================================================================
    # TIMESTAMP FIELDS - Audit trail and scheduling
    # ========================================================================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # published_at = models.DateTimeField(
    #     blank=True,
    #     null=True,
    #     help_text="When the job was published/activated"
    # )
    # expires_at = models.DateTimeField(
    #     blank=True,
    #     null=True,
    #     help_text="When the job posting expires"
    # )

    # ========================================================================
    # META CONFIGURATION
    # ========================================================================
    class Meta:
        db_table = 'jobs'
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        ordering = ['-created_at']
        indexes = [
            # models.Index(fields=['status', 'is_active']),
            models.Index(fields=['location']),
            models.Index(fields=['job_type']),
            models.Index(fields=['experience_level']),
        ]

    # ========================================================================
    # STRING REPRESENTATION
    # ========================================================================
    def __str__(self):
        return f"{self.title} at {self.company.name}"

    # ========================================================================
    # COMPUTED PROPERTIES - Derived fields for easy access
    # ========================================================================
    
    @property
    def salary_range(self):
        """
        Returns a formatted salary range string
        
        USAGE: range_text = job.salary_range # display salary information
        RETURNS: String with salary range or "Salary not specified"
        """
        if self.salary_min and self.salary_max:
            return f"${self.salary_min:,.0f} - ${self.salary_max:,.0f} {self.salary_currency}"
        elif self.salary_min:
            return f"From ${self.salary_min:,.0f} {self.salary_currency}"
        elif self.salary_max:
            return f"Up to ${self.salary_max:,.0f} {self.salary_currency}"
        return "Salary not specified"

    @property
    def is_expired(self):
        """
        Checks if the job posting has expired
        
        USAGE: if job.is_expired: # hide expired jobs
        RETURNS: Boolean indicating if job has expired
        """
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    @property
    def can_apply(self):
        """
        Determines if job is accepting applications
        
        USAGE: if job.can_apply: # show apply button
        RETURNS: Boolean indicating if applications are accepted
        """
        return (
            # self.status == 'active' and
            self.is_active and
            not self.is_expired and
            # (self.max_applications is None or 
            #  self.applications.count() < self.max_applications)
            True
        )

    @property
    def applications_count(self):
        """
        Returns the current number of applications
        
        USAGE: count = job.applications_count # show application count
        RETURNS: Integer count of applications
        """
        return self.applications.count()

    # ========================================================================
    # BUSINESS LOGIC METHODS - Job-specific operations
    # ========================================================================
    
    def activate(self):
        """
        Activates the job posting and sets published timestamp
        
        USAGE: job.activate() # make job visible to job seekers
        SIDE EFFECTS: Updates status, published_at, and is_active
        """
        # self.status = 'active'
        self.is_active = True
        # self.published_at = timezone.now()
        self.save()

    def pause(self):
        """
        Pauses the job posting temporarily
        
        USAGE: job.pause() # temporarily hide job from job seekers
        SIDE EFFECTS: Updates status and is_active
        """
        # self.status = 'paused'
        self.is_active = False
        self.save()

    def close(self):
        """
        Closes the job posting to new applications
        
        USAGE: job.close() # stop accepting new applications
        SIDE EFFECTS: Updates status and is_active
        """
        # self.status = 'closed'
        self.is_active = False
        self.save()

    def fill(self):
        """
        Marks the job as filled
        
        USAGE: job.fill() # indicate position has been filled
        SIDE EFFECTS: Updates status and is_active
        """
        # self.status = 'filled'
        self.is_active = False
        self.save()

    def get_application_deadline_status(self):
        """
        Returns the status of the application deadline
        
        USAGE: status = job.get_application_deadline_status() # show deadline info
        RETURNS: String indicating deadline status
        """
        if not self.application_deadline:
            return "No deadline"
        
        now = timezone.now()
        if now > self.application_deadline:
            return "Deadline passed"
        elif now.date() == self.application_deadline.date():
            return "Deadline today"
        else:
            days_left = (self.application_deadline - now).days
            return f"{days_left} days left"

# =============================================================================
# THROUGH MODELS - MANY-TO-MANY RELATIONSHIP TABLES
# =============================================================================
# These models manage the many-to-many relationships between jobs and
# categories/skills, allowing for additional metadata on the relationships.
# =============================================================================

class JobCategoryJob(models.Model):
    """
    Through Model - Manages Job-Category relationships
    
    PURPOSE: Links jobs to categories with additional metadata
    RELATIONSHIP: Many-to-many between Job and JobCategory
    """
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    
    # Additional metadata
    is_primary = models.BooleanField(
        default=False,
        help_text="Whether this is the primary category for the job"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'job_category_job'
        unique_together = ['job', 'category']

    def __str__(self):
        return f"{self.job.title} - {self.category.name}"

class JobSkillJob(models.Model):
    """
    Through Model - Manages Job-Skill relationships
    
    PURPOSE: Links jobs to skills with requirement level and importance
    RELATIONSHIP: Many-to-many between Job and JobSkill
    """
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    skill = models.ForeignKey(JobSkill, on_delete=models.CASCADE)
    
    # Skill requirement details
    is_required = models.BooleanField(
        default=True,
        help_text="Whether this skill is required or preferred"
    )
    
    proficiency_level = models.CharField(
        max_length=20,
        choices=JobSkill.SKILL_LEVEL_CHOICES,
        blank=True,
        help_text="Required proficiency level for this skill"
    )
    
    years_experience = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Years of experience required for this skill"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'job_skill_job'
        unique_together = ['job', 'skill']

    def __str__(self):
        requirement = "Required" if self.is_required else "Preferred"
        return f"{self.job.title} - {self.skill.name} ({requirement})" 