from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Notification, NotificationTemplate, UserNotificationPreference
from .serializers import NotificationSerializer, NotificationTemplateSerializer, UserNotificationPreferenceSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_list(request):
    """List notifications for the current user"""
    notifications = Notification.objects.filter(user_id=request.user.id).order_by('-created_at')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_detail(request, notification_id):
    """Get notification details"""
    notification = get_object_or_404(Notification, id=notification_id, user_id=request.user.id)
    serializer = NotificationSerializer(notification)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_as_read(request, notification_id):
    """Mark notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, user_id=request.user.id)
    notification.status = 'read'
    notification.save()
    return Response({'status': 'marked as read'})


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def notification_preferences(request):
    """Get or update notification preferences"""
    if request.method == 'GET':
        preferences = UserNotificationPreference.objects.filter(user_id=request.user.id)
        serializer = UserNotificationPreferenceSerializer(preferences, many=True)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Update preferences
        for preference_data in request.data:
            preference, created = UserNotificationPreference.objects.get_or_create(
                user_id=request.user.id,
                notification_type=preference_data['notification_type']
            )
            preference.is_enabled = preference_data.get('is_enabled', True)
            preference.save()
        
        return Response({'status': 'preferences updated'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def template_list(request):
    """List notification templates"""
    templates = NotificationTemplate.objects.filter(is_active=True)
    serializer = NotificationTemplateSerializer(templates, many=True)
    return Response(serializer.data) 