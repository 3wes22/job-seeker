from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('<int:notification_id>/', views.notification_detail, name='notification_detail'),
    path('<int:notification_id>/read/', views.mark_as_read, name='mark_as_read'),
    path('preferences/', views.notification_preferences, name='notification_preferences'),
    path('templates/', views.template_list, name='template_list'),
] 