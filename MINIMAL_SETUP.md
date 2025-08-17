# 🚀 Minimal Backend Setup for Flutter App

This setup provides only the essential backend services needed to run your Flutter app with minimal resource usage.

## 📋 What's Included

### ✅ **Essential Services (Required)**
- **PostgreSQL Database** - User data storage
- **User Service** - Authentication, registration, user management
- **Redis** - Session management (optional but recommended)

### ❌ **Services NOT Included (Not needed yet)**
- Job Service - Not implemented in Flutter app
- Application Service - Not implemented in Flutter app  
- Search Service - Not implemented in Flutter app
- Notification Service - Not implemented in Flutter app
- Analytics Service - Not implemented in Flutter app
- API Gateway - Not configured to use

## 🚀 Quick Start

### 1. **Start Minimal Services**
```bash
./scripts/start_minimal_backend.sh
```

This will:
- Start PostgreSQL database
- Start Redis
- Install Python dependencies
- Run database migrations
- Start User Service on port 8001

### 2. **Check Service Status**
```bash
./scripts/check_minimal_backend.sh
```

### 3. **Stop Services**
```bash
./scripts/stop_minimal_backend.sh
```

## 🔧 Manual Setup (Alternative)

If you prefer to start services manually:

### Start Database
```bash
docker-compose -f docker-compose.minimal.yml up -d
```

### Start User Service
```bash
cd backend/user-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8001
```

## 📱 Flutter App Configuration

Your Flutter app is already configured to connect to:
- **User Service**: `http://10.0.2.2:8001` (Android Emulator)
- **User Service**: `http://localhost:8001` (iOS Simulator/Web)

## 🗄️ Database Access

- **Host**: localhost
- **Port**: 5432
- **Database**: job_platform
- **Username**: postgres
- **Password**: postgres123

## 🔍 Troubleshooting

### Service Not Starting
1. Check if Docker is running
2. Check if ports 8001, 5432, 6379 are available
3. Check logs: `docker-compose -f docker-compose.minimal.yml logs`

### Database Connection Issues
1. Wait for database to be ready (health check)
2. Check if migrations ran successfully
3. Verify database credentials in user service settings

### User Service Issues
1. Check if virtual environment is activated
2. Verify all dependencies are installed
3. Check if database is accessible

## 📈 When to Add More Services

Add these services as you implement them in your Flutter app:

- **Job Service**: When you add job posting/searching
- **Application Service**: When you add job applications
- **Search Service**: When you add advanced search features
- **Notification Service**: When you add push notifications
- **Analytics Service**: When you add user analytics

## 💾 Resource Usage

**Minimal Setup:**
- PostgreSQL: ~50-100MB RAM
- Redis: ~10-20MB RAM  
- User Service: ~50-100MB RAM
- **Total**: ~110-220MB RAM

**Full Setup** (all services): ~500MB+ RAM
