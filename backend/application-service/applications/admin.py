from django.contrib import admin
from .models import Application, ApplicationAttachment, ApplicationStatusHistory, Interview


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_id', 'applicant_id', 'employer_id', 'status', 'is_active', 'created_at')
    list_filter = ('status', 'is_active', 'created_at')
    search_fields = ('job_id', 'applicant_id', 'employer_id')
    ordering = ('-created_at',)


@admin.register(ApplicationAttachment)
class ApplicationAttachmentAdmin(admin.ModelAdmin):
    list_display = ('application', 'file_name', 'file_type', 'file_size', 'created_at')
    list_filter = ('file_type', 'created_at')
    search_fields = ('file_name', 'application__id')
    ordering = ('-created_at',)


@admin.register(ApplicationStatusHistory)
class ApplicationStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('application', 'status', 'changed_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('application__id', 'notes')
    ordering = ('-created_at',)


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('application', 'interview_type', 'scheduled_at', 'status', 'created_at')
    list_filter = ('interview_type', 'status', 'created_at')
    search_fields = ('application__id', 'location', 'notes')
    ordering = ('-scheduled_at',) 