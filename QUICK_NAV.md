# 🚀 Quick Navigation Guide

## 🔧 **Backend Services**

### **User Service** (Port 8001)
- **Models:** `backend/user-service/users/models.py`
- **Views:** `backend/user-service/users/views.py` 
- **URLs:** `backend/user-service/users/urls.py`
- **Settings:** `backend/user-service/user_service/settings.py`

### **Job Service** (Port 8002)
- **Models:** `backend/job-service/jobs/models.py`
- **Views:** `backend/job-service/jobs/views.py`
- **URLs:** `backend/job-service/jobs/urls.py`

### **Application Service** (Port 8003)
- **Models:** `backend/application-service/applications/models.py`
- **Views:** `backend/application-service/applications/views.py`
- **URLs:** `backend/application-service/applications/urls.py`

### **Search Service** (Port 8004)
- **Models:** `backend/search-service/search/models.py`
- **Views:** `backend/search-service/search/views.py`

### **Notification Service** (Port 8005)
- **Models:** `backend/notification-service/notifications/models.py`
- **Views:** `backend/notification-service/notifications/views.py`

### **Analytics Service** (Port 8006)
- **Models:** `backend/analytics-service/analytics/models.py`
- **Views:** `backend/analytics-service/analytics/views.py`

## 📱 **Flutter Frontend**

### **Core Files**
- **Main:** `frontend/flutter-app/lib/main.dart`
- **Router:** `frontend/flutter-app/lib/core/router/app_router.dart`
- **Config:** `frontend/flutter-app/lib/core/config/app_config.dart`
- **Providers:** `frontend/flutter-app/lib/core/di/providers.dart`

### **Services**
- **API Service:** `frontend/flutter-app/lib/shared/services/api_service.dart`
- **Auth Service:** `frontend/flutter-app/lib/shared/services/auth_service.dart`
- **Job Service:** `frontend/flutter-app/lib/shared/services/job_service.dart`
- **Application Service:** `frontend/flutter-app/lib/shared/services/application_service.dart`

### **Models**
- **User:** `frontend/flutter-app/lib/shared/models/user_model.dart`
- **Job:** `frontend/flutter-app/lib/shared/models/job_model.dart`
- **Application:** `frontend/flutter-app/lib/shared/models/application_model.dart`

### **Pages**
- **Login:** `frontend/flutter-app/lib/features/auth/presentation/pages/login_page.dart`
- **Register:** `frontend/flutter-app/lib/features/auth/presentation/pages/register_page.dart`
- **Home:** `frontend/flutter-app/lib/features/home/presentation/pages/home_page.dart`
- **Post Job:** `frontend/flutter-app/lib/features/jobs/presentation/pages/post_job_page.dart`
- **Job Search:** `frontend/flutter-app/lib/features/jobs/presentation/pages/job_search_page.dart`
- **Applications:** `frontend/flutter-app/lib/features/applications/presentation/pages/applications_page.dart`
- **Profile:** `frontend/flutter-app/lib/features/profile/presentation/pages/profile_page.dart`

## 🐳 **Infrastructure**
- **Docker Compose:** `docker-compose.yml`
- **API Gateway:** `infrastructure/docker/api-gateway/nginx.conf`
- **Setup Script:** `scripts/setup_development.sh`

## 🚀 **Quick Commands**
```bash
# Start all services
docker-compose up -d

# Start specific service
cd backend/user-service && python manage.py runserver 0.0.0.0:8001

# Flutter app
cd frontend/flutter-app && flutter run
```

## 📋 **File Search Tips**
Use **Ctrl/Cmd + P** in your editor and type:
- `models.py` → Backend data models
- `views.py` → Backend API logic  
- `*.dart` → Flutter files
- `settings.py` → Configuration files
- `urls.py` → API routing
