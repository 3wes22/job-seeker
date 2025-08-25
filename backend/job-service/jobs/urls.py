from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    # Job-related endpoints
    path('', views.job_list, name='job_list'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('create/', views.job_create, name='job_create'),
    path('<int:job_id>/update/', views.job_update, name='job_update'),
    path('<int:job_id>/delete/', views.job_delete, name='job_delete'),
    path('<int:job_id>/withdraw/', views.job_withdraw, name='job_withdraw'),
    
    # Employer-specific endpoints
    path('employer/', views.employer_jobs, name='employer_jobs'),
    
    # Company-related endpoints
    path('companies/', views.company_list, name='company_list'),
    path('companies/<int:company_id>/', views.company_detail, name='company_detail'),
    path('companies/create/', views.company_create, name='company_create'),
    
    # Category and skill endpoints
    path('categories/', views.category_list, name='category_list'),
    path('skills/', views.skill_list, name='skill_list'),
] 