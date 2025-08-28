from .models import Job, Company
# from .models import Job, Company, JobCategory, JobSkill, JobCategoryJob, JobSkillJob
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


# class JobCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = JobCategory
#         fields = '__all__'


# class JobSkillSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = JobSkill
#         fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name', read_only=True)
    company_id = serializers.IntegerField(write_only=True)
    # categories = JobCategorySerializer(many=True, read_only=True)  # Commented out - table doesn't exist
    # skills = JobSkillSerializer(many=True, read_only=True)  # Commented out - table doesn't exist
    salary_min = serializers.FloatField(read_only=True)
    salary_max = serializers.FloatField(read_only=True)
    employer = serializers.SerializerMethodField()
    skills_required = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'requirements', 'company', 'company_id', 'employer_id',
            'job_type', 'experience_level', 'location', 'is_remote', 'salary_min',
            'salary_max', 'salary_range', 'employer', 'skills_required', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_employer(self, obj):
        """Return a dummy employer object structure for Flutter compatibility"""
        return {
            'id': obj.employer_id,
            'name': f'Employer {obj.employer_id}',
            'email': f'employer{obj.employer_id}@example.com',
            'user_type': 'employer'
        }
    
    def get_skills_required(self, obj):
        """Extract skills from requirements text for Flutter compatibility"""
        if obj.requirements:
            # Simple skill extraction - split by common delimiters
            skills = []
            requirements = obj.requirements.lower()
            
            # Common programming languages and skills
            common_skills = [
                'python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go',
                'swift', 'kotlin', 'react', 'angular', 'vue', 'node.js', 'django',
                'flask', 'spring', 'laravel', 'rails', 'docker', 'kubernetes',
                'aws', 'azure', 'gcp', 'sql', 'mongodb', 'redis', 'git'
            ]
            
            for skill in common_skills:
                if skill in requirements:
                    skills.append(skill.title())
            
            # If no common skills found, extract words that might be skills
            if not skills:
                words = requirements.split()
                # Filter words that look like skills (capitalized, 3+ chars)
                potential_skills = [word.title() for word in words 
                                 if len(word) >= 3 and word[0].isupper()]
                skills.extend(potential_skills[:5])  # Limit to 5 skills
            
            return skills
        return []
    
    def validate(self, attrs):
        """Validate job data"""
        errors = {}
        
        # Validate salary range
        salary_min = attrs.get('salary_min')
        salary_max = attrs.get('salary_max')
        
        if salary_min and salary_max and salary_min > salary_max:
            errors['salary_range'] = 'Minimum salary cannot be greater than maximum salary'
        
        # Validate required fields
        required_fields = ['title', 'description', 'company_id', 'employer_id']
        for field in required_fields:
            if not attrs.get(field):
                errors[field] = f'{field.replace("_", " ").title()} is required'
        
        if errors:
            raise ValidationError(errors)
        
        return attrs
    
    def create(self, validated_data):
        """Create a new job with category and skill relationships"""
        # Extract category and skill IDs if provided
        category_ids = self.context.get('category_ids', [])
        skill_ids = self.context.get('skill_ids', [])
        
        # Handle company_id to company mapping
        if 'company_id' in validated_data:
            company_id = validated_data.pop('company_id')
            try:
                from .models import Company
                company = Company.objects.get(id=company_id)
                validated_data['company'] = company
            except Company.DoesNotExist:
                raise ValidationError({'company_id': f'Company with id {company_id} does not exist'})
        
        # Create the job
        job = Job.objects.create(**validated_data)
        
        # Add categories if provided
        if category_ids:
            try:
                for category_id in category_ids:
                    # category = JobCategory.objects.get(id=category_id)
                    # JobCategoryJob.objects.create(job=job, category=category)
                    pass  # Temporarily disabled
            except Exception as e:
                print(f"Warning: Could not add categories: {e}")
        
        # Add skills if provided
        if skill_ids:
            try:
                for skill_data in skill_ids:
                    if isinstance(skill_data, dict):
                        skill_id = skill_data.get('skill_id')
                        is_required = skill_data.get('is_required', True)
                    else:
                        skill_id = skill_data
                        is_required = True
                    
                    # skill = JobSkill.objects.get(id=skill_id)
                    # JobSkillJob.objects.create(job=job, skill=skill, is_required=is_required)
                    pass  # Temporarily disabled
            except Exception as e:
                print(f"Warning: Could not add skills: {e}")
        
        return job 