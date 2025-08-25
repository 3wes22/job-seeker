# 🚀 Kafka Integration Documentation

## Overview

This document describes the complete Kafka integration implementation for the Job Platform microservices architecture. The integration enables real-time, event-driven communication between services, providing loose coupling and scalability.

## 🏗️ Architecture

### Event Flow Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Service  │    │   Job Service   │    │  Other Services │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │   Models    │ │    │ │   Models    │ │    │ │   Models    │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
│        │        │    │        │        │    │        │        │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │   Signals   │ │    │ │   Signals   │ │    │ │   Signals   │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
│        │        │    │        │        │    │        │        │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │   Events    │ │    │ │   Events    │ │    │ │   Events    │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
│        │        │    │        │        │    │        │        │
└────────┼────────┘    └────────┼────────┘    └────────┼────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                        KAFKA CLUSTER                           │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │user-events  │  │ job-events  │  │other-events │            │
│  │   Topic     │  │   Topic     │  │   Topic     │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│         ▲                ▲                ▲                   │
│         │                │                │                   │
│         ▼                ▼                ▼                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   User      │  │    Job      │  │   Other     │            │
│  │  Consumer   │  │  Consumer   │  │  Consumer   │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

### Key Components

1. **Event Publishers**: Django signals trigger events when models change
2. **Kafka Topics**: Dedicated topics for different event types
3. **Event Consumers**: Services consume events from other services
4. **Event Schemas**: Structured event data with versioning

## 📋 Event Types

### User Service Events

| Event Type | Description | Triggered When | Data |
|------------|-------------|----------------|------|
| `user_created` | New user registered | User model created | User details, type, profile |
| `user_updated` | User profile updated | User model modified | User details, changes made |
| `user_deleted` | User account deleted | User model deleted | User ID, username |

### Job Service Events

| Event Type | Description | Triggered When | Data |
|------------|-------------|----------------|------|
| `job_created` | New job posted | Job model created | Job details, company, employer |
| `job_updated` | Job details updated | Job model modified | Job details, changes made |
| `job_deleted` | Job removed | Job model deleted | Job ID, employer ID |
| `job_status_changed` | Job status updated | Job status field changed | Old/new status, job details |
| `job_application_received` | New application | Application received | Job details, application count |

## 🛠️ Setup Instructions

### Prerequisites

- Docker and Docker Compose
- Python 3.8+
- Kafka knowledge (basic)

### Quick Setup

```bash
# 1. Clone and navigate to project
cd job-platform

# 2. Run the automated setup script
./scripts/setup_kafka_integration.sh

# 3. Verify setup
docker-compose ps
```

### Manual Setup

```bash
# 1. Start Kafka infrastructure
docker-compose up -d zookeeper kafka kafka-ui

# 2. Wait for Kafka to be ready (30 seconds)
sleep 30

# 3. Create Kafka topics
python3 scripts/setup_kafka_topics.py

# 4. Start backend services
docker-compose up -d

# 5. Start Kafka consumers
cd backend/user-service
python3 manage.py start_kafka_consumer &

cd ../job-service
python3 manage.py start_kafka_consumer &
```

## 🔧 Configuration

### Environment Variables

```bash
# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=kafka:29092
KAFKA_GROUP_ID=user-service-group

# Topics
KAFKA_TOPICS_USER_EVENTS=user-events
KAFKA_TOPICS_JOB_EVENTS=job-events
```

### Django Settings

```python
# settings.py
KAFKA_BOOTSTRAP_SERVERS = config('KAFKA_BOOTSTRAP_SERVERS', default='localhost:9092').split(',')
KAFKA_GROUP_ID = config('KAFKA_GROUP_ID', default='user-service-group')

KAFKA_TOPICS = {
    'USER_EVENTS': 'user-events',
    'JOB_EVENTS': 'job-events'
}
```

## 📊 Monitoring & Debugging

### Kafka UI

Access the Kafka UI at `http://localhost:8080` to:
- View topics and partitions
- Monitor message flow
- Inspect event data
- Check consumer groups

### Service Logs

```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f user-service
docker-compose logs -f job-service

# View Kafka logs
docker-compose logs -f kafka
```

### Consumer Status

```bash
# Check if consumers are running
ps aux | grep start_kafka_consumer

# Check consumer PIDs
cat backend/user-service/.user_consumer.pid
cat backend/job-service/.job_consumer.pid
```

## 🧪 Testing

### Integration Tests

```bash
# Run comprehensive Kafka integration tests
python3 scripts/test_kafka_integration.py

# Test with custom Kafka servers
python3 scripts/test_kafka_integration.py --bootstrap-servers localhost:9092
```

### Manual Testing

```bash
# 1. Start services
docker-compose up -d

# 2. Create a test user via API
curl -X POST http://localhost:8001/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass"}'

# 3. Check Kafka UI for events
# 4. Verify consumer logs
```

## 🔄 Event Flow Examples

### User Registration Flow

1. **User Service**: User model created → `user_created` event published
2. **Job Service**: Consumes `user_created` event → Creates default company profile
3. **Notification Service**: Consumes `user_created` event → Sends welcome email

### Job Posting Flow

1. **Job Service**: Job model created → `job_created` event published
2. **User Service**: Consumes `job_created` event → Updates employer statistics
3. **Search Service**: Consumes `job_created` event → Updates search index
4. **Notification Service**: Consumes `job_created` event → Notifies relevant job seekers

### Job Application Flow

1. **Application Service**: Application received → `job_application_received` event published
2. **Job Service**: Consumes event → Updates application count
3. **User Service**: Consumes event → Notifies employer
4. **Notification Service**: Consumes event → Sends confirmation emails

## 🚨 Troubleshooting

### Common Issues

#### 1. Kafka Connection Failed

```bash
# Check if Kafka is running
docker-compose ps kafka

# Check Kafka logs
docker-compose logs kafka

# Verify network connectivity
docker-compose exec user-service ping kafka
```

#### 2. Events Not Being Published

```bash
# Check Django signals
docker-compose logs user-service | grep "signal"

# Verify event publisher initialization
docker-compose logs user-service | grep "Event published"

# Check topic existence
docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --list
```

#### 3. Events Not Being Consumed

```bash
# Check consumer status
ps aux | grep start_kafka_consumer

# Check consumer logs
docker-compose logs user-service | grep "consumer"
docker-compose logs job-service | grep "consumer"

# Verify consumer group
docker-compose exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 --list
```

#### 4. High Memory Usage

```bash
# Check consumer memory usage
ps aux | grep start_kafka_consumer | awk '{print $6}'

# Restart consumers if needed
pkill -f start_kafka_consumer
# Then restart them manually
```

### Debug Mode

Enable debug logging in Django settings:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'kafka': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 📈 Performance & Scaling

### Optimization Tips

1. **Batch Processing**: Process events in batches for better throughput
2. **Connection Pooling**: Reuse Kafka connections
3. **Async Processing**: Use async/await for non-blocking operations
4. **Partitioning**: Use appropriate partition keys for load balancing

### Scaling Considerations

1. **Horizontal Scaling**: Run multiple consumer instances
2. **Partition Strategy**: Design partition keys for even distribution
3. **Consumer Groups**: Use different consumer groups for different use cases
4. **Monitoring**: Set up alerts for lag and throughput

## 🔒 Security

### Current Implementation

- **Authentication**: None (development setup)
- **Encryption**: None (development setup)
- **Authorization**: Service-level access control

### Production Recommendations

1. **SASL Authentication**: Implement SASL/PLAIN or SASL/SCRAM
2. **SSL/TLS Encryption**: Enable SSL for data in transit
3. **ACLs**: Configure Kafka Access Control Lists
4. **Audit Logging**: Log all event access and modifications

## 📚 API Reference

### Event Publisher

```python
from users.events import user_event_publisher

# Publish user created event
user_event_publisher.publish_user_created(user_instance)

# Publish user updated event
user_event_publisher.publish_user_updated(user_instance, changes_dict)
```

### Event Consumer

```python
from users.consumers import user_service_consumer

# Start consuming events
user_service_consumer.start_consuming()

# Stop consuming events
user_service_consumer.stop_consuming()
```

### Management Commands

```bash
# Start user service consumer
python3 manage.py start_kafka_consumer

# Start job service consumer
python3 manage.py start_kafka_consumer
```

## 🔮 Future Enhancements

### Planned Features

1. **Dead Letter Queues**: Handle failed event processing
2. **Event Replay**: Replay events for debugging/recovery
3. **Schema Registry**: Centralized event schema management
4. **Event Sourcing**: Complete audit trail of all changes
5. **CQRS**: Command Query Responsibility Segregation

### Integration Points

1. **Notification Service**: Real-time push notifications
2. **Analytics Service**: Event-driven analytics
3. **Search Service**: Real-time search index updates
4. **Payment Service**: Event-driven payment processing

## 📞 Support

### Getting Help

1. **Check Logs**: Always start with service and Kafka logs
2. **Verify Configuration**: Ensure all environment variables are set
3. **Test Connectivity**: Use the test scripts to verify integration
4. **Review Architecture**: Understand the event flow for your use case

### Useful Commands

```bash
# Health check
docker-compose ps

# Restart services
docker-compose restart user-service job-service

# View real-time logs
docker-compose logs -f --tail=100

# Check Kafka topics
docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --list

# Monitor consumer groups
docker-compose exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 --list
```

---

**Note**: This documentation covers the current implementation. For production deployments, additional security, monitoring, and scaling considerations should be implemented.
