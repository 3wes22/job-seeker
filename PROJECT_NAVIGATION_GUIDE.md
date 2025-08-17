# 🚀 Job Platform - Complete Navigation Guide

## 📁 **Project Overview**
A microservices-based job platform with Flutter frontend and Django backend services.

---

## 🏗️ **Backend Services Architecture**

### 🔐 **User Service** (`backend/user-service/`)
**Port:** 8001 | **Database:** postgres-users:5432/users_db

#### **Core Files:**
- **`users/models.py`** - User, Company, Profile models
- **`users/views.py`** - Authentication, registration, profile management
- **`users/serializers.py`** - JSON serialization for User/Company data
- **`users/urls.py`** - API endpoints routing
- **`users/consumers.py` - WebSocket consumers for real-time updates
- **`users/signals.py` - Django signals for user events
- **`user_service/settings.py`** - Service configuration, database, Kafka settings

#### **Key Endpoints:**
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration  
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/profile/` - Update profile
- `POST /api/companies/` - Create company

---

### 💼 **Job Service** (`backend/job-service/`)
**Port:** 8002 | **Database:** postgres-jobs:5432/jobs_db

#### **Core Files:**
- **`jobs/models.py`** - Job, Category, Skill, Company models
- **`jobs/views.py`** - Job CRUD, search, filtering
- **`jobs/serializers.py`** - Job data serialization
- **`jobs/urls.py`** - Job API endpoints
- **`jobs/signals.py`** - Job creation/update events
- **`job_service/settings.py`** - Service configuration

#### **Key Endpoints:**
- `GET /api/jobs/` - List all jobs
- `POST /api/jobs/` - Create new job
- `GET /api/jobs/{id}/` - Get job details
- `PUT /api/jobs/{id}/` - Update job
- `GET /api/categories/` - Job categories
- `GET /api/skills/` - Available skills

---

### 📝 **Application Service** (`backend/application-service/`)
**Port:** 8003 | **Database:** postgres-applications:5432/applications_db

#### **Core Files:**
- **`applications/models.py`** - Application, CoverLetter models
- **`applications/views.py`** - Application CRUD, status updates
- **`applications/serializers.py`** - Application data serialization
- **`applications/urls.py`** - Application API endpoints
- **`applications/signals.py`** - Application events
- **`application_service/settings.py`** - Service configuration

#### **Key Endpoints:**
- `GET /api/applications/` - List applications
- `POST /api/applications/` - Submit application
- `GET /api/applications/{id}/` - Get application details
- `PUT /api/applications/{id}/` - Update application status

---

### 🔍 **Search Service** (`backend/search-service/`)
**Port:** 8004 | **Database:** postgres-search:5432/search_db

#### **Core Files:**
- **`search/models.py`** - Search index models
- **`search/views.py`** - Search functionality, filters
- **`search/urls.py`** - Search API endpoints
- **`search/signals.py`** - Search index updates
- **`search_service/settings.py`** - Service configuration

#### **Key Endpoints:**
- `GET /api/search/jobs/` - Search jobs
- `GET /api/search/companies/` - Search companies
- `GET /api/search/users/` - Search users

---

### 🔔 **Notification Service** (`backend/notification-service/`)
**Port:** 8005 | **Database:** postgres-notifications:5432/notifications_db

#### **Core Files:**
- **`notifications/models.py`** - Notification, NotificationTemplate models
- **`notifications/views.py`** - Notification CRUD, sending
- **`notifications/serializers.py`** - Notification serialization
- **`notifications/urls.py`** - Notification API endpoints
- **`notifications/signals.py`** - Notification triggers
- **`notification_service/settings.py`** - Service configuration

#### **Key Endpoints:**
- `GET /api/notifications/` - List notifications
- `POST /api/notifications/` - Create notification
- `PUT /api/notifications/{id}/read/` - Mark as read

---

### 📊 **Analytics Service** (`backend/analytics-service/`)
**Port:** 8006 | **Database:** postgres-analytics:5432/analytics_db

#### **Core Files:**
- **`analytics/models.py`** - Analytics data models
- **`analytics/views.py`** - Analytics endpoints, metrics
- **`analytics/serializers.py`** - Analytics data serialization
- **`analytics/urls.py`** - Analytics API endpoints
- **`analytics/signals.py`** - Data collection triggers
- **`analytics_service/settings.py`** - Service configuration

#### **Key Endpoints:**
- `GET /api/analytics/jobs/` - Job analytics
- `GET /api/analytics/applications/` - Application metrics
- `GET /api/analytics/users/` - User behavior data

---

### 🌐 **API Gateway** (`infrastructure/docker/api-gateway/`)
**Port:** 8000

#### **Core Files:**
- **`nginx.conf`** - Routing rules, load balancing
- **`Dockerfile`** - Gateway container setup

---

### 🔧 **Shared Backend** (`backend/shared/`)
#### **Core Files:**
- **`events.py`** - Event definitions for Kafka
- **`kafka_utils.py`** - Kafka producer/consumer utilities
- **`service_registry.py`** - Service discovery
- **`settings.py`** - Common settings

---

## 📱 **Flutter Frontend Architecture** (`frontend/flutter-app/`)

### 🏠 **Core Structure** (`lib/core/`)

#### **Configuration** (`lib/core/config/`)
- **`app_config.dart`** - Environment config, API URLs, service endpoints

#### **Dependency Injection** (`lib/core/di/`)
- **`providers.dart`** - Riverpod providers for all services

#### **Network Layer** (`lib/core/network/`)
- **`http_client.dart`** - Base HTTP client with interceptors
- **`api_service.dart`** - Main API service with microservice routing

#### **Router** (`lib/core/router/`)
- **`app_router.dart`** - GoRouter configuration, all app routes

#### **Utils** (`lib/core/utils/`)
- **`result.dart`** - API response wrapper
- **`loading_state.dart`** - UI loading state management
- **`dev_tools.dart`** - Development utilities, debugging

---

### 🔐 **Authentication Feature** (`lib/features/auth/`)

#### **Presentation** (`lib/features/auth/presentation/`)
- **`pages/login_page.dart`** - Login screen UI and logic
- **`pages/register_page.dart`** - Registration screen
- **`widgets/auth_form.dart`** - Reusable auth form

#### **Domain** (`lib/features/auth/domain/`)
- **`repositories/auth_repository.dart`** - Auth business logic

#### **Data** (`lib/features/auth/data/`)
- **`datasources/auth_remote_data_source.dart`** - Auth API calls

---

### 💼 **Jobs Feature** (`lib/features/jobs/`)

#### **Presentation** (`lib/features/jobs/presentation/`)
- **`pages/job_list_page.dart`** - Job listing screen
- **`pages/job_detail_page.dart`** - Job details view
- **`pages/post_job_page.dart`** - Create new job
- **`pages/job_search_page.dart`** - Job search interface
- **`widgets/job_card.dart`** - Job display widget
- **`widgets/job_filter.dart`** - Job filtering controls

#### **Domain** (`lib/features/jobs/domain/`)
- **`repositories/job_repository.dart`** - Job business logic
- **`entities/job.dart`** - Job domain model

#### **Data** (`lib/features/jobs/data/`)
- **`datasources/job_remote_data_source.dart`** - Job API calls

---

### 📝 **Applications Feature** (`lib/features/applications/`)

#### **Presentation** (`lib/features/applications/presentation/`)
- **`pages/applications_page.dart`** - View applications
- **`pages/application_detail_page.dart`** - Application details
- **`widgets/application_card.dart`** - Application display
- **`widgets/application_status.dart`** - Status indicators

#### **Domain** (`lib/features/applications/domain/`)
- **`repositories/application_repository.dart`** - Application logic
- **`entities/application.dart`** - Application domain model

#### **Data** (`lib/features/applications/data/`)
- **`datasources/application_remote_data_source.dart`** - Application API

---

### 👤 **Profile Feature** (`lib/features/profile/`)

#### **Presentation** (`lib/features/profile/presentation/`)
- **`pages/profile_page.dart`** - User profile view
- **`pages/edit_profile_page.dart`** - Profile editing
- **`widgets/profile_header.dart`** - Profile header widget
- **`widgets/profile_stats.dart`** - User statistics

#### **Domain** (`lib/features/profile/domain/`)
- **`repositories/profile_repository.dart`** - Profile business logic
- **`entities/profile.dart`** - Profile domain model

#### **Data** (`lib/features/profile/data/`)
- **`datasources/profile_remote_data_source.dart`** - Profile API

---

### 🏠 **Home Feature** (`lib/features/home/`)

#### **Presentation** (`lib/features/home/presentation/`)
- **`pages/home_page.dart`** - Main dashboard
- **`widgets/dashboard_widget.dart`** - Dashboard overview
- **`widgets/quick_actions.dart`** - Quick action buttons

---

### 🔄 **Shared Components** (`lib/shared/`)

#### **Services** (`lib/shared/services/`)
- **`auth_service.dart`** - Authentication service
- **`job_service.dart`** - Job API service
- **`application_service.dart`** - Application API service
- **`notification_service.dart`** - Notification service

#### **Models** (`lib/shared/models/`)
- **`user_model.dart`** - User data model
- **`job_model.dart`** - Job data model
- **`application_model.dart`** - Application data model
- **`company_model.dart`** - Company data model

#### **Providers** (`lib/shared/providers/`)
- **`auth_providers.dart`** - Auth state providers
- **`job_providers.dart`** - Job state providers
- **`application_providers.dart`** - Application state providers

#### **Widgets** (`lib/shared/widgets/`)
- **`loading_indicator.dart`** - Loading spinners
- **`error_widget.dart`** - Error display widgets
- **`empty_state.dart`** - Empty state displays

---

## 🐳 **Infrastructure & DevOps**

### **Docker Configuration**
- **`docker-compose.yml`** - All services orchestration
- **`infrastructure/docker/`** - Service-specific Dockerfiles

### **Scripts** (`scripts/`)
- **`setup_development.sh`** - Complete dev environment setup
- **`load_dummy_data.py`** - Test data generation
- **`resume_setup.sh`** - Resume interrupted setup

---

## 🔑 **Key Navigation Shortcuts**

### **Quick Backend Access:**
- **User Service:** `backend/user-service/users/views.py` (line ~20)
- **Job Service:** `backend/job-service/jobs/views.py` (line ~15)
- **Application Service:** `backend/application-service/applications/views.py` (line ~10)

### **Quick Frontend Access:**
- **Main App:** `frontend/flutter-app/lib/main.dart` (line ~25)
- **Router:** `frontend/flutter-app/lib/core/router/app_router.dart` (line ~15)
- **API Service:** `frontend/flutter-app/lib/shared/services/api_service.dart` (line ~30)

### **Configuration Files:**
- **Docker:** `docker-compose.yml` (line ~1)
- **Flutter Config:** `frontend/flutter-app/pubspec.yaml` (line ~1)
- **Backend Settings:** `backend/user-service/user_service/settings.py` (line ~1)

---

## 🚀 **Development Workflow**

### **1. Start Backend Services:**
```bash
cd backend/user-service && python manage.py runserver 0.0.0.0:8001
cd backend/job-service && python manage.py runserver 0.0.0.0:8002
cd backend/application-service && python manage.py runserver 0.0.0.0:8003
```

### **2. Start Infrastructure:**
```bash
docker-compose up -d postgres-users postgres-jobs postgres-applications redis kafka
```

### **3. Start Flutter App:**
```bash
cd frontend/flutter-app && flutter run
```

---

## 📋 **File Quick Reference**

| **Category** | **Key Files** | **Purpose** |
|--------------|---------------|-------------|
| **Backend Models** | `*/models.py` | Data structure definitions |
| **Backend Views** | `*/views.py` | API endpoint logic |
| **Backend URLs** | `*/urls.py` | API routing |
| **Frontend Pages** | `*/pages/*.dart` | UI screens |
| **Frontend Services** | `shared/services/*.dart` | API communication |
| **Frontend Models** | `shared/models/*.dart` | Data models |
| **Configuration** | `*/settings.py`, `app_config.dart` | App settings |
| **Routing** | `app_router.dart` | Navigation logic |

---

## 🎯 **Common Development Tasks**

### **Add New API Endpoint:**
1. **Backend:** Add to `*/models.py` → `*/serializers.py` → `*/views.py` → `*/urls.py`
2. **Frontend:** Add to `shared/services/*.dart` → `shared/models/*.dart` → `features/*/presentation/`

### **Add New Flutter Page:**
1. Create in `features/*/presentation/pages/`
2. Add route in `core/router/app_router.dart`
3. Update navigation in relevant pages

### **Database Changes:**
1. Modify `*/models.py`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`

---

This guide provides instant access to every core component in your project. Use **Ctrl/Cmd + P** in your editor and type the filename to jump directly to any file! 🎯
