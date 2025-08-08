from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    # Application endpoints
    path('', views.application_list, name='application_list'),
    path('<int:application_id>/', views.application_detail, name='application_detail'),
    path('create/', views.application_create, name='application_create'),
    path('<int:application_id>/update/', views.application_update, name='application_update'),
    path('<int:application_id>/delete/', views.application_delete, name='application_delete'),
    
    # Interview endpoints
    path('<int:application_id>/interviews/', views.interview_list, name='interview_list'),
    path('<int:application_id>/interviews/create/', views.interview_create, name='interview_create'),
    path('interviews/<int:interview_id>/', views.interview_detail, name='interview_detail'),
    path('interviews/<int:interview_id>/update/', views.interview_update, name='interview_update'),
] 