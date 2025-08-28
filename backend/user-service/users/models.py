from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# =============================================================================
# USER MODEL - CORE USER ENTITY FOR THE JOB PLATFORM
# =============================================================================
# This model extends Django's AbstractUser to provide custom user functionality
# for both job seekers and employers. It includes additional fields for profile
# management, verification, and user type classification.
# =============================================================================

class User(AbstractUser):
    """
    Custom User Model - Core entity for authentication and user management
    
    EXTENDS: Django AbstractUser (username, email, password, first_name, last_name)
    PURPOSE: Handles both job seekers and employers with role-based access
    
    KEY FEATURES:
    - Phone number for contact
    - Date of birth for age verification
    - Profile picture for visual identification
    - Bio for self-description
    - User type classification (job_seeker/employer)
    - Verification status for security
    - Timestamps for audit trails
    """
    
    # ========================================================================
    # USER TYPE CHOICES - Defines the two main user categories
    # ========================================================================
    USER_TYPE_CHOICES = [
        ('job_seeker', 'Job Seeker'),      # Individual looking for jobs
        ('employer', 'Employer'),          # Company/recruiter posting jobs
    ]
    
    # ========================================================================
    # CORE USER FIELDS - Additional fields beyond Django's AbstractUser
    # ========================================================================
    
    # Contact Information
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        help_text="User's phone number for contact purposes"
    )
    
    # Personal Information
    date_of_birth = models.DateField(
        blank=True, 
        null=True,
        help_text="Date of birth for age verification and demographics"
    )
    
    # Profile Media
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        blank=True, 
        null=True,
        help_text="User's profile picture for visual identification"
    )
    
    # Self Description
    bio = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        default="",
        help_text="User's biography or description"
    )
    
    # Role Classification
    user_type = models.CharField(
        max_length=20, 
        choices=USER_TYPE_CHOICES, 
        default='job_seeker',
        help_text="Determines user role: job seeker or employer"
    )
    
    # Security & Verification
    is_verified = models.BooleanField(
        default=False,
        help_text="Indicates if user account has been verified"
    )
    
    # Account Status
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates if user account is active"
    )
    
    # ========================================================================
    # TIMESTAMP FIELDS - Audit trail for user actions
    # ========================================================================
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when user account was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when user account was last updated"
    )

    # ========================================================================
    # META CONFIGURATION - Django model settings
    # ========================================================================
    class Meta:
        db_table = 'users'  # Custom table name
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']  # Newest users first

    # ========================================================================
    # STRING REPRESENTATION - How user appears in admin and logs
    # ========================================================================
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    # ========================================================================
    # COMPUTED PROPERTIES - Derived fields for easy access
    # ========================================================================
    
    @property
    def full_name(self):
        """
        Returns the user's full name combining first and last name
        
        USAGE: user.full_name instead of f"{user.first_name} {user.last_name}"
        RETURNS: String with full name or username if names are empty
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @property
    def age(self):
        """
        Calculates user's age based on date of birth
        
        USAGE: user.age to get current age
        RETURNS: Integer age or None if DOB not set
        """
        if self.dob:
            today = timezone.now().date()
            return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return None

    @property
    def is_job_seeker(self):
        """
        Quick check if user is a job seeker
        
        USAGE: if user.is_job_seeker: # show job search features
        RETURNS: Boolean indicating job seeker status
        """
        return self.user_type == 'job_seeker'

    @property
    def is_employer(self):
        """
        Quick check if user is an employer
        
        USAGE: if user.is_employer: # show job posting features
        RETURNS: Boolean indicating employer status
        """
        return self.user_type == 'employer'

    # ========================================================================
    # BUSINESS LOGIC METHODS - User-specific operations
    # ========================================================================
    
    def can_post_jobs(self):
        """
        Determines if user has permission to post jobs
        
        RULES: Only verified employers can post jobs
        USAGE: if user.can_post_jobs(): # show job posting form
        RETURNS: Boolean indicating job posting permission
        """
        return self.is_employer and self.is_verified

    def can_apply_for_jobs(self):
        """
        Determines if user has permission to apply for jobs
        
        RULES: Only verified job seekers can apply
        USAGE: if user.can_apply_for_jobs(): # show apply button
        RETURNS: Boolean indicating job application permission
        """
        return self.is_job_seeker and self.is_verified

    def get_profile_completeness(self):
        """
        Calculates profile completion percentage
        
        USAGE: progress = user.get_profile_completeness() # show progress bar
        RETURNS: Integer percentage (0-100) of profile completion
        """
        required_fields = ['first_name', 'last_name', 'email', 'phone']
        optional_fields = ['dob', 'bio', 'profile_picture']
        
        completed_required = sum(1 for field in required_fields if getattr(self, field))
        completed_optional = sum(1 for field in optional_fields if getattr(self, field))
        
        required_weight = 0.7  # 70% weight for required fields
        optional_weight = 0.3  # 30% weight for optional fields
        
        required_score = (completed_required / len(required_fields)) * required_weight
        optional_score = (completed_optional / len(optional_fields)) * optional_weight
        
        return int((required_score + optional_score) * 100)

# =============================================================================
# COMPANY MODEL - REPRESENTS EMPLOYER ORGANIZATIONS
# =============================================================================
# This model stores company information for employers posting jobs.
# It's linked to the User model through a one-to-one relationship.
# =============================================================================

class Company(models.Model):
    """
    Company Model - Represents employer organizations posting jobs
    
    RELATIONSHIP: One-to-one with User (employer)
    PURPOSE: Stores company details for job postings and employer profiles
    
    KEY FEATURES:
    - Company identification and contact info
    - Industry classification
    - Company size and location
    - Company description and branding
    - Verification status for trust
    """
    
    # ========================================================================
    # COMPANY SIZE CHOICES - Standard company size classifications
    # ========================================================================
    COMPANY_SIZE_CHOICES = [
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501-1000', '501-1000 employees'),
        ('1000+', '1000+ employees'),
    ]
    
    # ========================================================================
    # CORE COMPANY FIELDS - Essential company information
    # ========================================================================
    
    # Company Identification
    name = models.CharField(
        max_length=200,
        help_text="Official company name"
    )
    
    # Company Details
    industry = models.CharField(
        max_length=100,
        blank=True,
        help_text="Primary industry sector"
    )
    
    company_size = models.CharField(
        max_length=20,
        choices=COMPANY_SIZE_CHOICES,
        blank=True,
        help_text="Number of employees"
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
        help_text="Company website URL"
    )
    
    # Company Description
    description = models.TextField(
        blank=True,
        help_text="Company description and mission"
    )
    
    # Verification Status
    is_verified = models.BooleanField(
        default=False,
        help_text="Indicates if company has been verified"
    )
    
    # ========================================================================
    # RELATIONSHIPS - Links to other models
    # ========================================================================
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='company',
        help_text="Associated user account (employer)"
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
        db_table = 'companies'
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['-created_at']

    # ========================================================================
    # STRING REPRESENTATION
    # ========================================================================
    def __str__(self):
        return f"{self.name} ({self.get_company_size_display()})"

    # ========================================================================
    # BUSINESS LOGIC METHODS
    # ========================================================================
    
    def get_job_count(self):
        """
        Returns the number of jobs posted by this company
        
        USAGE: job_count = company.get_job_count() # show in company profile
        RETURNS: Integer count of active jobs
        """
        # Note: This will work once Job model is imported
        # from jobs.models import Job
        # return Job.objects.filter(company=self, is_active=True).count()
        return 0  # Placeholder until Job model is available

    def get_employee_count(self):
        """
        Returns the employee count as an integer
        
        USAGE: count = company.get_employee_count() # for calculations
        RETURNS: Integer employee count or None if not set
        """
        if self.company_size:
            # Extract numbers from choices like "51-200"
            import re
            numbers = re.findall(r'\d+', self.company_size)
            if numbers:
                return int(numbers[-1])  # Return the higher number
        return None

# =============================================================================
# PROFILE MODEL - EXTENDED USER PROFILE INFORMATION
# =============================================================================
# This model stores additional profile information that might not be
# needed for every user interaction, keeping the User model lean.
# =============================================================================

class Profile(models.Model):
    """
    Profile Model - Extended user profile information
    
    RELATIONSHIP: One-to-one with User
    PURPOSE: Stores additional profile data without cluttering User model
    
    KEY FEATURES:
    - Professional summary
    - Social media links
    - Preferences and settings
    - Extended personal information
    """
    
    # ========================================================================
    # CORE PROFILE FIELDS
    # ========================================================================
    
    # Professional Information
    professional_summary = models.TextField(
        blank=True,
        max_length=1000,
        help_text="Professional summary and career objectives"
    )
    
    # Social Media
    linkedin_url = models.URLField(
        blank=True,
        help_text="LinkedIn profile URL"
    )
    
    github_url = models.URLField(
        blank=True,
        help_text="GitHub profile URL"
    )
    
    # Preferences
    email_notifications = models.BooleanField(
        default=True,
        help_text="Enable email notifications"
    )
    
    push_notifications = models.BooleanField(
        default=True,
        help_text="Enable push notifications"
    )
    
    # ========================================================================
    # RELATIONSHIPS
    # ========================================================================
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        help_text="Associated user account"
    )
    
    # ========================================================================
    # TIMESTAMP FIELDS
    # ========================================================================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ========================================================================
    # META CONFIGURATION
    # ========================================================================
    class Meta:
        db_table = 'profiles'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    # ========================================================================
    # STRING REPRESENTATION
    # ========================================================================
    def __str__(self):
        return f"Profile for {self.user.username}"

    # ========================================================================
    # BUSINESS LOGIC METHODS
    # ========================================================================
    
    def get_social_links(self):
        """
        Returns a dictionary of available social media links
        
        USAGE: links = profile.get_social_links() # display social icons
        RETURNS: Dict with available social media URLs
        """
        links = {}
        if self.linkedin_url:
            links['linkedin'] = self.linkedin_url
        if self.github_url:
            links['github'] = self.github_url
        return links
