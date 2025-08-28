# 🧪 Phase 1 Comprehensive Testing Guide

## 📋 **Testing Overview**

This document provides a systematic approach to test all working endpoints and functionality in Phase 1 of the Job Platform project. The goal is to ensure a solid foundation before proceeding to Phase 2.

## 🎯 **Testing Objectives**

- ✅ **Verify all microservices are running correctly**
- ✅ **Test all API endpoints and responses**
- ✅ **Validate JWT authentication flow**
- ✅ **Test complete job application workflow**
- ✅ **Verify Flutter app integration**
- ✅ **Document any remaining issues**

## 🚀 **Pre-Testing Setup**

### **1. Start All Required Services**

```bash
# Terminal 1: User Service
cd backend/user-service
source venv/bin/activate
python manage.py runserver 0.0.0.0:8001

# Terminal 2: Job Service  
cd backend/job-service
source venv/bin/activate
python manage.py runserver 0.0.0.0:8002

# Terminal 3: Application Service
cd backend/application-service
source venv/bin/activate
python manage.py runserver 0.0.0.0:8003

# Terminal 4: PostgreSQL (if not running)
brew services start postgresql@14
```

### **2. Verify Service Health**

```bash
# Check if all services are responding
curl -s http://localhost:8001/api/users/ | head -5
curl -s http://localhost:8002/api/jobs/ | head -5
curl -s http://localhost:8003/api/applications/check-status/1/ -H "Authorization: Bearer test" | head -5
```

## 🧪 **Testing Checklist**

### **Phase 1: Service Health & Basic Connectivity**

#### **1.1 User Service (Port 8001)**
- [ ] **Service Running**: `http://localhost:8001/` responds
- [ ] **Admin Access**: `http://localhost:8001/admin/` accessible
- [ **Database Connection**: No database errors in logs
- [ ] **Virtual Environment**: Python dependencies installed correctly

#### **1.2 Job Service (Port 8002)**
- [ ] **Service Running**: `http://localhost:8002/` responds
- [ ] **Admin Access**: `http://localhost:8002/admin/` accessible
- [ ] **Database Connection**: No database errors in logs
- [ ] **Test Data**: Jobs exist in database

#### **1.3 Application Service (Port 8003)**
- [ ] **Service Running**: `http://localhost:8003/` responds
- [ ] **Admin Access**: `http://localhost:8003/admin/` accessible
- [ ] **Database Connection**: No database errors in logs
- [ ] **Migrations Applied**: All database tables created

### **Phase 2: API Endpoint Testing**

#### **2.1 User Service Endpoints**

##### **Registration Endpoint**
```bash
# Test user registration
curl -X POST http://localhost:8001/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser_$(date +%s)",
    "email": "test$(date +%s)@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "user_type": "job_seeker",
    "phone_number": "+1234567890",
    "date_of_birth": "1990-01-01"
  }'
```

**Expected Result**: `201 Created` with user data and JWT tokens

##### **Login Endpoint**
```bash
# Test user login
curl -X POST http://localhost:8001/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

**Expected Result**: `200 OK` with user data and JWT tokens

##### **Profile Endpoint**
```bash
# Test profile retrieval (requires valid token)
TOKEN="YOUR_ACCESS_TOKEN_HERE"
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8001/api/users/profile/
```

**Expected Result**: `200 OK` with user profile data

#### **2.2 Job Service Endpoints**

##### **Job List Endpoint**
```bash
# Test job listing
curl -s http://localhost:8002/api/jobs/ | python3 -m json.tool
```

**Expected Result**: `200 OK` with array of job objects

##### **Job Detail Endpoint**
```bash
# Test job detail (assuming job ID 1 exists)
curl -s http://localhost:8002/api/jobs/1/ | python3 -m json.tool
```

**Expected Result**: `200 OK` with detailed job object

##### **Job Creation Endpoint (Admin)**
```bash
# Test job creation (requires admin user)
curl -X POST http://localhost:8002/api/jobs/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "title": "Test Job",
    "description": "Test job description",
    "requirements": "Python, Django",
    "responsibilities": "Develop web applications",
    "job_type": "full_time",
    "experience_level": "mid",
    "location": "Remote",
    "is_remote": true,
    "salary_min": 60000,
    "salary_max": 80000,
    "salary_currency": "USD",
    "company": "Test Company",
    "employer_id": 1,
    "is_active": true
  }'
```

**Expected Result**: `201 Created` with job data

#### **2.3 Application Service Endpoints**

##### **Application Status Check**
```bash
# Test application status check (requires valid token)
curl -s -H "Authorization: Bearer $TOKEN" \
  http://localhost:8003/api/applications/check-status/1/
```

**Expected Result**: `200 OK` with application status

##### **Application Creation**
```bash
# Test job application creation
curl -X POST http://localhost:8003/api/applications/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "job_id": 1,
    "employer_id": 1,
    "cover_letter": "I am interested in this position",
    "expected_salary": 70000,
    "availability_date": "2025-09-01"
  }'
```

**Expected Result**: `201 Created` with application data

##### **User Applications List**
```bash
# Test user applications listing
curl -s -H "Authorization: Bearer $TOKEN" \
  http://localhost:8003/api/applications/my-applications/
```

**Expected Result**: `200 OK` with user's applications

### **Phase 3: JWT Authentication Testing**

#### **3.1 Token Validation**
```bash
# Test token validation
curl -s -H "Authorization: Bearer $TOKEN" \
  http://localhost:8001/api/users/profile/
```

**Expected Result**: `200 OK` with user data

#### **3.2 Token Refresh**
```bash
# Test token refresh
curl -X POST http://localhost:8001/api/users/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "'$REFRESH_TOKEN'"}'
```

**Expected Result**: `200 OK` with new access token

#### **3.3 Invalid Token Handling**
```bash
# Test invalid token rejection
curl -s -H "Authorization: Bearer invalid_token" \
  http://localhost:8001/api/users/profile/
```

**Expected Result**: `401 Unauthorized`

### **Phase 4: Data Flow Testing**

#### **4.1 Complete User Journey**
1. **Register User** → Get tokens
2. **Login User** → Verify authentication
3. **Browse Jobs** → View job listings
4. **View Job Details** → Get specific job information
5. **Apply for Job** → Submit application
6. **Check Application Status** → Verify application created
7. **View User Applications** → List all applications

#### **4.2 Data Consistency Checks**
- [ ] **User ID Consistency**: Same user ID across all services
- [ ] **Job ID Consistency**: Job IDs match between services
- [ ] **Application Data**: Application data correctly stored and retrieved
- [ ] **Token Persistence**: Tokens work across all services

### **Phase 5: Flutter App Testing**

#### **5.1 App Launch & Navigation**
- [ ] **App Starts**: Flutter app launches without errors
- [ ] **Login Screen**: Login form displays correctly
- [ ] **Registration Screen**: Registration form displays correctly
- [ ] **Home Screen**: Home screen loads after authentication
- [ ] **Job List**: Job listings display correctly
- [ ] **Job Details**: Job detail view works
- [ ] **Application Flow**: Complete application submission works

#### **5.2 API Integration**
- [ ] **Authentication**: Login/registration works with backend
- [ ] **Job Loading**: Jobs load from backend API
- [ ] **Application Submission**: Applications submit successfully
- [ ] **Error Handling**: Proper error messages displayed
- [ ] **Loading States**: Loading indicators work correctly

## 🛠️ **Automated Testing Script**

I'll create a comprehensive testing script that automates most of these tests:

```bash
# Run comprehensive testing
python3 test_phase1_comprehensive.py
```

## 📊 **Testing Results Template**

### **Service Health Results**
| Service | Status | Issues | Notes |
|---------|--------|--------|-------|
| User Service (8001) | ⏳ | - | - |
| Job Service (8002) | ⏳ | - | - |
| Application Service (8003) | ⏳ | - | - |

### **API Endpoint Results**
| Endpoint | Status | Response Time | Issues |
|----------|--------|---------------|--------|
| User Registration | ⏳ | - | - |
| User Login | ⏳ | - | - |
| Job Listing | ⏳ | - | - |
| Application Creation | ⏳ | - | - |

### **Authentication Results**
| Test | Status | Issues | Notes |
|------|--------|--------|-------|
| Token Generation | ⏳ | - | - |
| Token Validation | ⏳ | - | - |
| Token Refresh | ⏳ | - | - |
| Invalid Token Rejection | ⏳ | - | - |

## 🚨 **Common Issues & Solutions**

### **Service Not Starting**
```bash
# Check if port is already in use
lsof -i :8001
lsof -i :8002
lsof -i :8003

# Kill process if needed
kill -9 <PID>
```

### **Database Connection Issues**
```bash
# Check PostgreSQL status
brew services list | grep postgresql

# Start PostgreSQL if needed
brew services start postgresql@14
```

### **Virtual Environment Issues**
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## ✅ **Success Criteria**

### **All Tests Must Pass**
- [ ] **Service Health**: All 3 services running and responding
- [ ] **API Endpoints**: All endpoints return correct status codes
- [ ] **Authentication**: JWT flow works end-to-end
- [ ] **Data Flow**: Complete user journey works
- [ ] **Flutter Integration**: App works with all backend services

### **Performance Requirements**
- **API Response Time**: < 500ms for all endpoints
- **Database Queries**: < 100ms for simple queries
- **App Launch Time**: < 3 seconds
- **Screen Load Time**: < 2 seconds

## 📝 **Next Steps After Testing**

1. **Document Results**: Record all test results and issues
2. **Fix Issues**: Resolve any remaining problems
3. **Performance Optimization**: Optimize slow endpoints
4. **Phase 2 Planning**: Begin planning next development phase
5. **Team Review**: Share results with development team

---

## 🔄 **Testing Schedule**

- **Day 1**: Service health and basic connectivity
- **Day 2**: API endpoint testing and validation
- **Day 3**: JWT authentication and data flow testing
- **Day 4**: Flutter app integration testing
- **Day 5**: Issue resolution and optimization

---

*This testing guide ensures we have a solid foundation before proceeding to Phase 2. All tests should pass before considering Phase 1 complete.*
