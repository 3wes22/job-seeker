from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from .models import AnalyticsEvent, UserAnalytics, JobAnalytics, PlatformAnalytics
from .serializers import AnalyticsEventSerializer, UserAnalyticsSerializer, JobAnalyticsSerializer, PlatformAnalyticsSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def analytics_events(request):
    """Create analytics events"""
    serializer = AnalyticsEventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_analytics(request):
    """Get user analytics"""
    user_id = request.GET.get('user_id', request.user.id)
    metric_name = request.GET.get('metric_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    queryset = UserAnalytics.objects.filter(user_id=user_id)
    
    if metric_name:
        queryset = queryset.filter(metric_name=metric_name)
    
    if start_date:
        queryset = queryset.filter(metric_date__gte=start_date)
    
    if end_date:
        queryset = queryset.filter(metric_date__lte=end_date)
    
    serializer = UserAnalyticsSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_analytics(request):
    """Get job analytics"""
    job_id = request.GET.get('job_id')
    metric_name = request.GET.get('metric_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    queryset = JobAnalytics.objects.all()
    
    if job_id:
        queryset = queryset.filter(job_id=job_id)
    
    if metric_name:
        queryset = queryset.filter(metric_name=metric_name)
    
    if start_date:
        queryset = queryset.filter(metric_date__gte=start_date)
    
    if end_date:
        queryset = queryset.filter(metric_date__lte=end_date)
    
    serializer = JobAnalyticsSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def platform_analytics(request):
    """Get platform analytics"""
    metric_name = request.GET.get('metric_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    queryset = PlatformAnalytics.objects.all()
    
    if metric_name:
        queryset = queryset.filter(metric_name=metric_name)
    
    if start_date:
        queryset = queryset.filter(metric_date__gte=start_date)
    
    if end_date:
        queryset = queryset.filter(metric_date__lte=end_date)
    
    serializer = PlatformAnalyticsSerializer(queryset, many=True)
    return Response(serializer.data) 