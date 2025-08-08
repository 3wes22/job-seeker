from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('events/', views.analytics_events, name='analytics_events'),
    path('user/', views.user_analytics, name='user_analytics'),
    path('job/', views.job_analytics, name='job_analytics'),
    path('platform/', views.platform_analytics, name='platform_analytics'),
] 