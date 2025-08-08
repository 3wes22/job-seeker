# Job Platform - Microservice Database Design

## Overview

This document outlines the database design for the job platform following microservice architecture principles. Each service will have its own dedicated database to ensure loose coupling and independent scalability.

## Microservice Database Architecture

### 1. User Service Database (`users_db`)

**Purpose**: Manages user accounts, authentication, and user profiles.

#### Tables:

```sql
-- Users table (extends Django's AbstractUser)
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    phone_number VARCHAR(15),
    date_of_birth DATE,
    profile_picture VARCHAR(255),
    bio TEXT,
    user_type VARCHAR(20) DEFAULT 'job_seeker' CHECK (user_type IN ('job_seeker', 'employer', 'admin')),
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User verification tokens
CREATE TABLE user_verification_tokens (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    token_type VARCHAR(50) NOT NULL, -- 'email_verification', 'password_reset'
    expires_at TIMESTAMP NOT NULL,
    used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User sessions (for JWT token blacklisting)
CREATE TABLE user_sessions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    refresh_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Job Service Database (`jobs_db`)

**Purpose**: Manages job postings, company information, and job-related data.

#### Tables:

```sql
-- Companies table
CREATE TABLE companies (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    website VARCHAR(255),
    logo VARCHAR(255),
    industry VARCHAR(100),
    size VARCHAR(50), -- 'startup', 'small', 'medium', 'large'
    founded_year INTEGER,
    location VARCHAR(255),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Jobs table
CREATE TABLE jobs (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT,
    responsibilities TEXT,
    company_id BIGINT REFERENCES companies(id) ON DELETE CASCADE,
    employer_id BIGINT NOT NULL, -- References user_id from user-service
    job_type VARCHAR(50) DEFAULT 'full_time' CHECK (job_type IN ('full_time', 'part_time', 'contract', 'internship', 'freelance')),
    experience_level VARCHAR(50) DEFAULT 'entry' CHECK (experience_level IN ('entry', 'mid', 'senior', 'executive')),
    salary_min DECIMAL(10,2),
    salary_max DECIMAL(10,2),
    salary_currency VARCHAR(3) DEFAULT 'USD',
    location VARCHAR(255),
    is_remote BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    application_deadline DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Job categories
CREATE TABLE job_categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    parent_id BIGINT REFERENCES job_categories(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Job-category relationships
CREATE TABLE job_categories_jobs (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT REFERENCES jobs(id) ON DELETE CASCADE,
    category_id BIGINT REFERENCES job_categories(id) ON DELETE CASCADE,
    UNIQUE(job_id, category_id)
);

-- Job skills
CREATE TABLE job_skills (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Job-skill relationships
CREATE TABLE job_skills_jobs (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT REFERENCES jobs(id) ON DELETE CASCADE,
    skill_id BIGINT REFERENCES job_skills(id) ON DELETE CASCADE,
    is_required BOOLEAN DEFAULT FALSE,
    UNIQUE(job_id, skill_id)
);
```

### 3. Application Service Database (`applications_db`)

**Purpose**: Manages job applications, application status, and application-related data.

#### Tables:

```sql
-- Applications table
CREATE TABLE applications (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL, -- References job from job-service
    applicant_id BIGINT NOT NULL, -- References user_id from user-service
    employer_id BIGINT NOT NULL, -- References user_id from user-service
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'reviewing', 'shortlisted', 'interviewing', 'offered', 'hired', 'rejected', 'withdrawn')),
    cover_letter TEXT,
    expected_salary DECIMAL(10,2),
    availability_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Application attachments
CREATE TABLE application_attachments (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT REFERENCES applications(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(100),
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Application status history
CREATE TABLE application_status_history (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT REFERENCES applications(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL,
    notes TEXT,
    changed_by BIGINT NOT NULL, -- References user_id from user-service
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Interviews table
CREATE TABLE interviews (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT REFERENCES applications(id) ON DELETE CASCADE,
    interview_type VARCHAR(50) DEFAULT 'phone' CHECK (interview_type IN ('phone', 'video', 'in_person')),
    scheduled_at TIMESTAMP,
    duration_minutes INTEGER DEFAULT 60,
    location VARCHAR(255),
    notes TEXT,
    status VARCHAR(50) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'completed', 'cancelled', 'rescheduled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Search Service Database (`search_db`)

**Purpose**: Manages search indexes, search history, and search-related analytics.

#### Tables:

```sql
-- Search indexes (for full-text search)
CREATE TABLE search_indexes (
    id BIGSERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL, -- 'job', 'company', 'user'
    entity_id BIGINT NOT NULL,
    search_vector tsvector,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Search history
CREATE TABLE search_history (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL, -- References user_id from user-service
    query TEXT NOT NULL,
    filters JSONB,
    results_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Search analytics
CREATE TABLE search_analytics (
    id BIGSERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    search_count INTEGER DEFAULT 1,
    last_searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Notification Service Database (`notifications_db`)

**Purpose**: Manages notifications, email templates, and notification preferences.

#### Tables:

```sql
-- Notifications table
CREATE TABLE notifications (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL, -- References user_id from user-service
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(50) NOT NULL, -- 'email', 'push', 'sms', 'in_app'
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'failed', 'read')),
    metadata JSONB,
    sent_at TIMESTAMP,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notification templates
CREATE TABLE notification_templates (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    subject VARCHAR(255),
    body TEXT NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User notification preferences
CREATE TABLE user_notification_preferences (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL, -- References user_id from user-service
    notification_type VARCHAR(50) NOT NULL,
    is_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, notification_type)
);
```

### 6. Analytics Service Database (`analytics_db`)

**Purpose**: Manages analytics data, metrics, and reporting.

#### Tables:

```sql
-- Analytics events
CREATE TABLE analytics_events (
    id BIGSERIAL PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    user_id BIGINT, -- References user_id from user-service (nullable for anonymous events)
    session_id VARCHAR(255),
    properties JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User analytics
CREATE TABLE user_analytics (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL, -- References user_id from user-service
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,2),
    metric_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Job analytics
CREATE TABLE job_analytics (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL, -- References job from job-service
    metric_name VARCHAR(100) NOT NULL,
    metric_value INTEGER DEFAULT 0,
    metric_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Platform analytics
CREATE TABLE platform_analytics (
    id BIGSERIAL PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,2),
    metric_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Database Design Principles

### 1. Service Isolation
- Each service has its own dedicated database
- No direct database sharing between services
- Services communicate via APIs only

### 2. Data Ownership
- User Service owns all user-related data
- Job Service owns job and company data
- Application Service owns application data
- Each service is responsible for its own data consistency

### 3. Eventual Consistency
- Services can have eventual consistency for cross-service data
- Use event-driven architecture for data synchronization
- Implement saga pattern for distributed transactions

### 4. Scalability
- Each database can be scaled independently
- Use read replicas for read-heavy operations
- Implement caching strategies (Redis)

### 5. Data Replication Strategy
- User data can be replicated to other services as needed
- Use event sourcing for audit trails
- Implement CQRS pattern for read/write separation

## Cross-Service Data Relationships

### 1. User References
- Other services reference users by `user_id` (BIGINT)
- User data is replicated via events when needed
- User service is the source of truth for user information

### 2. Job References
- Application service references jobs by `job_id` (BIGINT)
- Job data is replicated via events when needed
- Job service is the source of truth for job information

### 3. Event-Driven Synchronization
- Use message queues (RabbitMQ/Apache Kafka) for events
- Implement event sourcing for data consistency
- Use saga pattern for distributed transactions

## Migration Strategy

### Phase 1: Service Isolation
1. Separate existing monolithic database into service-specific databases
2. Implement service boundaries
3. Set up event-driven communication

### Phase 2: Data Optimization
1. Optimize each service's database schema
2. Implement caching strategies
3. Set up read replicas

### Phase 3: Advanced Features
1. Implement CQRS pattern
2. Add event sourcing
3. Implement advanced analytics

## Security Considerations

1. **Database Access**: Each service only has access to its own database
2. **Encryption**: All sensitive data should be encrypted at rest
3. **Network Security**: Use private networks for database communication
4. **Audit Logging**: Implement comprehensive audit trails
5. **Data Privacy**: Implement data retention and deletion policies

## Monitoring and Observability

1. **Database Metrics**: Monitor each database's performance
2. **Service Dependencies**: Track cross-service dependencies
3. **Data Consistency**: Monitor eventual consistency
4. **Error Tracking**: Implement comprehensive error tracking
5. **Performance Monitoring**: Monitor query performance and optimization 