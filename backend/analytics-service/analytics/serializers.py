from rest_framework import serializers
from .models import AnalyticsEvent, UserAnalytics, JobAnalytics, PlatformAnalytics


class AnalyticsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsEvent
        fields = '__all__'
        read_only_fields = ['timestamp']


class UserAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnalytics
        fields = '__all__'
        read_only_fields = ['created_at']


class JobAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAnalytics
        fields = '__all__'
        read_only_fields = ['created_at']


class PlatformAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformAnalytics
        fields = '__all__'
        read_only_fields = ['created_at'] 