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
    company = CompanySerializer(read_only=True)
    categories = JobCategorySerializer(many=True, read_only=True)
    skills = JobSkillSerializer(many=True, read_only=True)
    salary_range = serializers.ReadOnlyField()
    
    class Meta:
        model = Job
        fields = '__all__'
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