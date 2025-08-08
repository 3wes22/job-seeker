from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search, name='search'),
    path('history/', views.search_history, name='search_history'),
    path('analytics/', views.search_analytics, name='search_analytics'),
] 