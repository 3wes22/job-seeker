from django.contrib import admin
from .models import Notification, NotificationTemplate, UserNotificationPreference


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'notification_type', 'is_active', 'created_at')
    list_filter = ('notification_type', 'is_active', 'created_at')
    search_fields = ('name', 'subject', 'body')
    ordering = ('name',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'title', 'notification_type', 'status', 'created_at')
    list_filter = ('notification_type', 'status', 'created_at')
    search_fields = ('title', 'message', 'user_id')
    ordering = ('-created_at',)


@admin.register(UserNotificationPreference)
class UserNotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'notification_type', 'is_enabled', 'created_at')
    list_filter = ('notification_type', 'is_enabled', 'created_at')
    search_fields = ('user_id',)
    ordering = ('user_id', 'notification_type') 