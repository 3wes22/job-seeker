from rest_framework import serializers
from .models import Job, Company, JobCategory, JobSkill, JobCategoryJob, JobSkillJob


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = '__all__'
        read_only_fields = ['created_at']


class JobSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSkill
        fields = '__all__'
        read_only_fields = ['created_at']


class JobSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name', read_only=True, help_text="Company name for this job")
    # categories = JobCategorySerializer(many=True, read_only=True)  # Commented out - table doesn't exist
    # skills = JobSkillSerializer(many=True, read_only=True)  # Commented out - table doesn't exist
    salary_min = serializers.FloatField(read_only=True)
    salary_max = serializers.FloatField(read_only=True)
    salary_range = serializers.ReadOnlyField()
    
    # Add employer field that returns a User object structure
    employer = serializers.SerializerMethodField()
    
    # Add skills_required field that the Flutter app expects
    skills_required = serializers.SerializerMethodField()
    
    def get_employer(self, obj):
        # Return a basic user structure that the Flutter app expects
        return {
            'id': obj.employer_id,
            'username': f'user_{obj.employer_id}',
            'email': f'user{obj.employer_id}@example.com',
            'user_type': 'employer'
        }
    
    def get_skills_required(self, obj):
        # Extract skills from requirements field and return as array
        if obj.requirements:
            # Split requirements by common delimiters and clean up
            skills = obj.requirements.replace(',', ' ').replace(';', ' ').split()
            # Filter out common words and keep technical terms
            technical_skills = [skill.strip() for skill in skills if len(skill.strip()) > 2 and skill.strip().lower() not in ['and', 'the', 'for', 'with', 'experience', 'required', 'skills', 'knowledge']]
            return technical_skills[:5]  # Return max 5 skills
        return []
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'requirements', 'responsibilities',
            'job_type', 'experience_level', 'location', 'is_remote',
            'salary_min', 'salary_max', 'salary_currency', 'company',
            'employer_id', 'employer', 'skills_required', 'created_at', 'updated_at', 'is_active', 'salary_range'
        ]
        read_only_fields = ['created_at', 'updated_at', 'employer_id']
    
    def create(self, validated_data):
        # Handle many-to-many relationships
        categories_data = self.context.get('categories', [])
        skills_data = self.context.get('skills', [])
        
        job = Job.objects.create(**validated_data)
        
        # Add categories
        for category_id in categories_data:
            try:
                category = JobCategory.objects.get(id=category_id)
                JobCategoryJob.objects.create(job=job, category=category)
            except JobCategory.DoesNotExist:
                pass
        
        # Add skills
        for skill_data in skills_data:
            skill_id = skill_data.get('skill_id')
            is_required = skill_data.get('is_required', False)
            try:
                skill = JobSkill.objects.get(id=skill_id)
                JobSkillJob.objects.create(job=job, skill=skill, is_required=is_required)
            except JobSkill.DoesNotExist:
                pass
        
        return job 