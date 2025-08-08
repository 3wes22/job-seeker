from django.contrib import admin
from .models import AnalyticsEvent, UserAnalytics, JobAnalytics, PlatformAnalytics


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'user_id', 'session_id', 'timestamp')
    list_filter = ('event_type', 'timestamp')
    search_fields = ('event_type', 'user_id', 'session_id')
    ordering = ('-timestamp',)


@admin.register(UserAnalytics)
class UserAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'metric_name', 'metric_value', 'metric_date', 'created_at')
    list_filter = ('metric_name', 'metric_date', 'created_at')
    search_fields = ('user_id', 'metric_name')
    ordering = ('-metric_date', 'metric_name')


@admin.register(JobAnalytics)
class JobAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'metric_name', 'metric_value', 'metric_date', 'created_at')
    list_filter = ('metric_name', 'metric_date', 'created_at')
    search_fields = ('job_id', 'metric_name')
    ordering = ('-metric_date', 'metric_name')


@admin.register(PlatformAnalytics)
class PlatformAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('metric_name', 'metric_value', 'metric_date', 'created_at')
    list_filter = ('metric_name', 'metric_date', 'created_at')
    search_fields = ('metric_name',)
    ordering = ('-metric_date', 'metric_name') 