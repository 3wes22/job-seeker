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
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'applicant_id', 'employer_id']
    
    def validate(self, attrs):
        # Check if user has already applied for this job
        job_id = attrs.get('job_id')
        applicant_id = self.context.get('applicant_id')
        
        if job_id and applicant_id:
            if Application.objects.filter(job_id=job_id, applicant_id=applicant_id, is_active=True).exists():
                raise serializers.ValidationError("You have already applied for this job.")
        
        return attrs 