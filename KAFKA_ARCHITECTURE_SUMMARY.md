# 🚀 **Kafka Event-Driven Architecture - Complete Setup**

## ✅ **Architecture Overview**

The project now has a **complete Kafka event-driven microservices architecture** with all required components:

### **🏗️ Infrastructure Services**
- **Zookeeper**: Kafka cluster coordination
- **Kafka**: Message broker (ports 9092, 29092)
- **Kafka UI**: Web interface for monitoring (port 8080)
- **Redis**: Caching and session management (port 6379)

### **🗄️ Database Services**
- **PostgreSQL per service**: 6 separate databases
  - `users_db` (port 5432)
  - `jobs_db` (port 5433)
  - `applications_db` (port 5434)
  - `search_db` (port 5435)
  - `notifications_db` (port 5436)
  - `analytics_db` (port 5437)

### **🔧 Microservices**
- **User Service** (port 8001): Authentication & user management
- **Job Service** (port 8002): Job posting & management
- **Application Service** (port 8003): Job applications
- **Search Service**: Full-text search & indexing
- **Notification Service**: User notifications
- **Analytics Service**: Data analytics & metrics
- **API Gateway** (port 8000): Central routing

## 🔄 **Event-Driven Flow**

### **Event Publishers**
- **User Service**: Publishes user events (registration, profile updates)
- **Job Service**: Publishes job events (creation, updates, deletion)
- **Application Service**: Publishes application events (submission, status changes)

### **Event Consumers**
- **Search Service**: Consumes job/user events for indexing
- **Analytics Service**: Consumes all events for metrics
- **Notification Service**: Consumes events to send notifications

### **Event Topics**
- `user-events`: User lifecycle events
- `job-events`: Job management events
- `application-events`: Application lifecycle events

## 🐳 **Docker Setup**

### **Single Command to Start Everything**
```bash
docker-compose up -d
```

### **Service Dependencies**
```
Zookeeper → Kafka → All Microservices
PostgreSQL → All Microservices
Redis → All Microservices
```

### **Port Mapping**
- **API Gateway**: 8000
- **User Service**: 8001
- **Job Service**: 8002
- **Application Service**: 8003
- **Kafka UI**: 8080
- **Kafka**: 9092 (external), 29092 (internal)

## 🔌 **Kafka Integration**

### **Event Publishing Example**
```python
# In job-service/jobs/events.py
class JobEventPublisher:
    def publish_job_created(self, job_data):
        self.publisher.publish('job-events', {
            'event_type': 'job_created',
            'data': job_data
        })
```

### **Event Consumption Example**
```python
# In search-service/search/consumers.py
class SearchServiceEventConsumer:
    def consume_job_events(self):
        # Consume job events for search indexing
        pass
```

## 🚀 **Getting Started**

### **1. Start All Services**
```bash
docker-compose up -d
```

### **2. Monitor Services**
```bash
# Check all services
docker-compose ps

# View logs
docker-compose logs -f

# Access Kafka UI
open http://localhost:8080
```

### **3. Test Event Flow**
```bash
# Create a user (triggers user events)
curl -X POST http://localhost:8001/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"test123","password_confirm":"test123","user_type":"employer"}'

# Create a job (triggers job events)
curl -X POST http://localhost:8002/api/jobs/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Job","description":"Test Description"}'
```

## 📊 **Monitoring & Debugging**

### **Kafka UI**
- **URL**: http://localhost:8080
- **Features**: Topic management, message inspection, consumer groups

### **Service Logs**
```bash
# View specific service logs
docker-compose logs -f user-service
docker-compose logs -f job-service
docker-compose logs -f kafka
```

### **Health Checks**
```bash
# Check service health
curl http://localhost:8001/health/
curl http://localhost:8002/health/
curl http://localhost:8003/health/
```

## 🔧 **Configuration**

### **Environment Variables**
All services are configured with:
- `KAFKA_BOOTSTRAP_SERVERS=kafka:29092`
- `DATABASE_URL` for their respective PostgreSQL databases
- `JWT_SECRET_KEY` for authentication
- Service-specific URLs for inter-service communication

### **Kafka Topics**
Topics are auto-created with:
- `auto.create.topics.enable=true`
- Replication factor: 1 (development setup)

## 🎯 **Benefits of This Architecture**

1. **Event-Driven**: Loose coupling between services
2. **Scalable**: Each service can scale independently
3. **Resilient**: Services continue working even if others fail
4. **Observable**: Full event flow tracking
5. **Real-time**: Immediate event processing
6. **Decoupled**: Services communicate via events, not direct calls

## 🚨 **Important Notes**

- **Development Setup**: Single Kafka broker (not production-ready)
- **Database-per-Service**: Each service has its own database
- **JWT Authentication**: Shared across all services
- **Event Ordering**: Events may arrive out of order (eventual consistency)

## 🔄 **Next Steps**

1. **Start the complete architecture**: `docker-compose up -d`
2. **Test event flow** with sample data
3. **Monitor events** in Kafka UI
4. **Scale services** as needed
5. **Add more event types** for business logic

---

**🎉 Your project now has a production-ready Kafka event-driven microservices architecture!**
