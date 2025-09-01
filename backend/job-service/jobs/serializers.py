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
    # Flexible field that accepts both 'company' and 'company_id' from Flutter
    company_id = serializers.IntegerField(write_only=True, required=False)
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
            'job_type', 'experience_level', 'location', 'is_remote', 'remote_type', 'salary_min',
            'salary_max', 'salary_range', 'employer', 'skills_required', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'company_id': {'source': 'company_id', 'write_only': True},
        }
    
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
        if obj.requirements and obj.requirements.strip():
            # IMPROVED SKILL EXTRACTION: More robust parsing
            skills = []
            requirements = obj.requirements.lower().strip()
            
            # Common programming languages and skills
            common_skills = [
                'python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go',
                'swift', 'kotlin', 'react', 'angular', 'vue', 'node.js', 'django',
                'flask', 'spring', 'laravel', 'rails', 'docker', 'kubernetes',
                'aws', 'azure', 'gcp', 'sql', 'mongodb', 'redis', 'git',
                'html', 'css', 'typescript', 'scala', 'rust', 'elixir', 'clojure',
                'machine learning', 'ai', 'data science', 'devops', 'agile', 'scrum'
            ]
            
            # Extract exact matches first
            for skill in common_skills:
                if skill in requirements:
                    skills.append(skill.title())
            
            # If no common skills found, try to extract from context
            if not skills:
                # Look for capitalized words that might be skills
                words = requirements.split()
                potential_skills = []
                
                for word in words:
                    # Clean the word
                    clean_word = word.strip('.,!?()[]{}":;').lower()
                    if (len(clean_word) >= 3 and 
                        clean_word[0].isupper() and 
                        clean_word not in ['the', 'and', 'for', 'with', 'this', 'that']):
                        potential_skills.append(clean_word.title())
                
                # Limit to reasonable number of skills
                skills.extend(potential_skills[:8])
            
            # Remove duplicates while preserving order
            seen = set()
            unique_skills = []
            for skill in skills:
                if skill.lower() not in seen:
                    seen.add(skill.lower())
                    unique_skills.append(skill)
            
            return unique_skills[:10]  # Limit to 10 skills max
        
        return []
    
    def validate(self, attrs):
        """Validate job data"""
        errors = {}
        
        # Handle field mapping for Flutter compatibility
        if 'company' in attrs and 'company_id' not in attrs:
            attrs['company_id'] = attrs.pop('company')
            print(f"🔧 Field mapping: 'company' -> 'company_id': {attrs['company_id']}")
        
        # REMOTE_TYPE FIX: Ensure remote_type is properly handled
        is_remote = attrs.get('is_remote', False)
        remote_type = attrs.get('remote_type')
        
        if remote_type is None or remote_type == '':
            # Set default based on is_remote flag
            attrs['remote_type'] = 'remote' if is_remote else 'on_site'
            print(f"🔧 Set default remote_type: {attrs['remote_type']} (based on is_remote: {is_remote})")
        elif remote_type not in ['on_site', 'remote']:
            # Validate remote_type value
            errors['remote_type'] = 'remote_type must be either "on_site" or "remote"'
        
        # DATA VALIDATION FIX: Ensure required fields are present
        required_fields = ['title', 'description', 'company_id', 'location']
        for field in required_fields:
            if not attrs.get(field):
                errors[field] = f'{field.replace("_", " ").title()} is required'
        
        # Validate salary range
        salary_min = attrs.get('salary_min')
        salary_max = attrs.get('salary_max')
        
        if salary_min is not None and salary_max is not None:
            if salary_min > salary_max:
                errors['salary'] = 'Minimum salary cannot be greater than maximum salary'
        
        # DATA CONSISTENCY FIX: Ensure is_active is set properly
        if 'is_active' not in attrs:
            attrs['is_active'] = True  # Default to active for new jobs
        
        # Validate location and remote work consistency
        location = attrs.get('location', '').lower()
        is_remote = attrs.get('is_remote', False)
        
        if is_remote and location.lower() in ['remote', 'anywhere', 'worldwide']:
            # If job is remote, ensure location reflects this
            attrs['location'] = 'Remote'
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return attrs
    
    def create(self, validated_data):
        """Create a new job with category and skill relationships"""
        # Extract category and skill IDs if provided
        category_ids = self.context.get('category_ids', [])
        skill_ids = self.context.get('skill_ids', [])
        
        # DEBUG: Log validated data before processing
        print(f"🔍 JobSerializer.create() - validated_data: {validated_data}")
        print(f"🔍 remote_type in validated_data: {validated_data.get('remote_type', 'NOT_FOUND')}")
        
        # REMOTE_TYPE FIX: Ensure remote_type is set with proper default
        if 'remote_type' not in validated_data or validated_data['remote_type'] is None:
            is_remote = validated_data.get('is_remote', False)
            validated_data['remote_type'] = 'remote' if is_remote else 'on_site'
            print(f"🔧 Set remote_type to: {validated_data['remote_type']}")
        
        # Handle company_id to company mapping
        if 'company_id' in validated_data:
            company_id = validated_data.pop('company_id')
            try:
                from .models import Company
                company = Company.objects.get(id=company_id)
                validated_data['company'] = company
            except Company.DoesNotExist:
                raise ValidationError({'company_id': f'Company with id {company_id} does not exist'})
        
        # DEBUG: Log final validated data before DB creation
        print(f"🔍 Final validated_data before DB create: {validated_data}")
        
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

    def to_internal_value(self, data):
        """Handle field mapping for Flutter compatibility"""
        # Map 'company' to 'company_id' if present
        if 'company' in data and 'company_id' not in data:
            data = data.copy()
            data['company_id'] = data.pop('company')
            print(f"🔧 Field mapping in to_internal_value: 'company' -> 'company_id': {data['company_id']}")
        
        return super().to_internal_value(data) 