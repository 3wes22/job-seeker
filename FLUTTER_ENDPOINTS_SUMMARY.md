# Flutter Backend Endpoints Summary

## API Gateway Access
**Base URL:** `http://localhost:8000`

All Flutter app endpoints are now accessible through the unified API Gateway with CORS headers enabled for mobile/web access.

## 🔐 Authentication Endpoints

### User Registration
```http
POST /api/users/register/
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com", 
    "password": "password123",
    "user_type": "job_seeker"
}
```

### User Login
```http
POST /api/users/login/
Content-Type: application/json

{
    "username": "testuser",
    "password": "password123"
}
```

**Response:** Returns JWT token and user details
```json
{
    "access": "jwt_token_here",
    "refresh": "refresh_token_here",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "user_type": "job_seeker"
    }
}
```

## 💼 Job Endpoints

### Get All Jobs
```http
GET /api/jobs/
```

**Response:** Returns array of jobs with company details
```json
[
    {
        "id": 1,
        "title": "Software Engineer",
        "description": "Full-stack development position",
        "requirements": "React, Node.js, Python",
        "location": "San Francisco, CA",
        "salary_range": "$80,000 - $120,000",
        "employment_type": "full_time",
        "is_active": true,
        "created_at": "2024-01-15T10:30:00Z",
        "company": {
            "id": 1,
            "name": "Tech Corp",
            "description": "Leading technology company",
            "location": "San Francisco, CA"
        }
    }
]
```

### Create Job (Employer Only)
```http
POST /api/jobs/create/
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "title": "Frontend Developer",
    "description": "React development position",
    "requirements": "React, JavaScript, CSS",
    "location": "Remote",
    "salary_range": "$70,000 - $90,000",
    "employment_type": "full_time"
}
```

### Get Job Details
```http
GET /api/jobs/{job_id}/
```

## 📝 Application Endpoints

### Apply for Job
```http
POST /api/applications/apply/
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "job_id": 1,
    "cover_letter": "I am interested in this position..."
}
```

### Get User Applications (Job Seeker)
```http
GET /api/applications/my-applications/
Authorization: Bearer <jwt_token>
```

**Response:** Returns applications submitted by the authenticated job seeker
```json
[
    {
        "id": 1,
        "job": {
            "id": 1,
            "title": "Software Engineer",
            "company": {
                "name": "Tech Corp"
            }
        },
        "status": "pending",
        "applied_at": "2024-01-16T14:20:00Z",
        "cover_letter": "I am interested in this position..."
    }
]
```

### Get Job Applications (Employer)
```http
GET /api/applications/job/{job_id}/
Authorization: Bearer <jwt_token>
```

**Response:** Returns candidates who applied for employer's job posting
```json
[
    {
        "id": 1,
        "user": {
            "id": 2,
            "username": "johndoe",
            "email": "john@example.com"
        },
        "status": "pending",
        "applied_at": "2024-01-16T14:20:00Z",
        "cover_letter": "I am interested in this position..."
    }
]
```

### Update Application Status (Employer Only)
```http
PUT /api/applications/{application_id}/status/
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "status": "accepted"
}
```

## ✅ Authentication Requirements

- **Public Endpoints:** `/api/users/register/`, `/api/users/login/`, `/api/jobs/` (GET)
- **Authenticated Endpoints:** All other endpoints require JWT token in Authorization header
- **Role-Based Access:**
  - Job Seekers: Can apply for jobs, view their applications
  - Employers: Can create jobs, view applications for their jobs, update application status

## 🚀 Flutter Integration Notes

1. **Base URL:** Use `http://localhost:8000` for all API calls
2. **CORS:** Headers are configured for cross-origin requests
3. **Authentication:** Store JWT token and include in Authorization header: `Bearer <token>`
4. **Error Handling:** 
   - 401: Authentication required/invalid
   - 403: Insufficient permissions
   - 404: Resource not found
   - 400: Bad request/validation errors

## 📊 Database Status

All services are running with test data intact:
- Users: Registration and login functional
- Jobs: Sample jobs available for browsing
- Applications: Application system fully operational
- Companies: Employer profiles linked to job postings

## 🔧 Development Ready

Backend is fully configured and ready for Flutter app integration with:
- ✅ User authentication (registration/login)
- ✅ Job listings and creation
- ✅ Job application system
- ✅ Employer candidate management
- ✅ Unified API Gateway access
- ✅ CORS headers for mobile/web access
- ✅ JWT token-based security
