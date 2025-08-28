from rest_framework import serializers
from .models import Application, ApplicationAttachment, Interview, ApplicationStatusHistory


class ApplicationAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationAttachment
        fields = '__all__'
        read_only_fields = ['created_at']


class ApplicationStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatusHistory
        fields = '__all__'
        read_only_fields = ['created_at']


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ApplicationSerializer(serializers.ModelSerializer):
    attachments = ApplicationAttachmentSerializer(many=True, read_only=True)
    interviews = InterviewSerializer(many=True, read_only=True)
    status_history = ApplicationStatusHistorySerializer(many=True, read_only=True)
    
    # Custom fields to handle null values for Flutter compatibility
    cover_letter = serializers.SerializerMethodField()
    expected_salary = serializers.SerializerMethodField()
    availability_date = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = [
            'id', 'job_id', 'applicant_id', 'employer_id', 'status',
            'cover_letter', 'expected_salary', 'availability_date',
            'is_active', 'created_at', 'updated_at',
            'attachments', 'interviews', 'status_history'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'applicant_id', 'status', 'is_active']
    
    def get_cover_letter(self, obj):
        """Return cover_letter or empty string if null"""
        return obj.cover_letter if obj.cover_letter is not None else ""
    
    def get_expected_salary(self, obj):
        """Return expected_salary or empty string if null"""
        return str(obj.expected_salary) if obj.expected_salary is not None else ""
    
    def get_availability_date(self, obj):
        """Return availability_date or empty string if null"""
        return obj.availability_date.isoformat() if obj.availability_date is not None else ""
    
    def validate(self, attrs):
        # Ensure proper data types for numeric fields
        if 'job_id' in attrs:
            try:
                attrs['job_id'] = int(attrs['job_id'])
            except (ValueError, TypeError):
                raise serializers.ValidationError({
                    'job_id': 'job_id must be a valid integer'
                })
        
        if 'employer_id' in attrs:
            try:
                attrs['employer_id'] = int(attrs['employer_id'])
            except (ValueError, TypeError):
                raise serializers.ValidationError({
                    'employer_id': 'employer_id must be a valid integer'
                })
        
        # Handle cover_letter field properly
        if 'cover_letter' in attrs and attrs['cover_letter'] is None:
            attrs['cover_letter'] = ''  # Convert None to empty string
        
        # Handle expected_salary field
        if 'expected_salary' in attrs and attrs['expected_salary'] is not None:
            try:
                # Ensure it's a valid decimal
                float(attrs['expected_salary'])
            except (ValueError, TypeError):
                raise serializers.ValidationError({
                    'expected_salary': 'expected_salary must be a valid number'
                })
        
        # Check if user has already applied for this job
        job_id = attrs.get('job_id')
        applicant_id = self.context.get('applicant_id')
        
        if job_id and applicant_id:
            if Application.objects.filter(job_id=job_id, applicant_id=applicant_id, is_active=True).exists():
                raise serializers.ValidationError({
                    'job_id': 'You have already applied for this job.'
                })
        
        return attrs
    
    def create(self, validated_data):
        """Create a new application with proper field handling"""
        # Get the applicant_id from context
        applicant_id = self.context.get('applicant_id')
        if not applicant_id:
            raise serializers.ValidationError("applicant_id is required")
        
        # Ensure required fields are present
        if 'job_id' not in validated_data:
            raise serializers.ValidationError("job_id is required")
        
        if 'employer_id' not in validated_data:
            raise serializers.ValidationError("employer_id is required")
        
        # Create the application
        application = Application.objects.create(
            job_id=validated_data['job_id'],
            applicant_id=applicant_id,
            employer_id=validated_data['employer_id'],
            cover_letter=validated_data.get('cover_letter', ''),
            expected_salary=validated_data.get('expected_salary'),
            availability_date=validated_data.get('availability_date'),
            status='pending',
            is_active=True
        )
        
        return application 