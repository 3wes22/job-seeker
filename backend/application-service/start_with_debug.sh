#!/bin/bash

# Application Service Startup Script with Debug Configuration
echo "🚀 Starting Application Service with Debug Configuration..."

# Set environment variables
export JWT_SECRET_KEY="django-insecure-jwt-secret-key-shared-across-services"
export DEBUG="True"
export SECRET_KEY="django-insecure-jwt-secret-key-shared-across-services"

# Database configuration
export DB_NAME="applications_db"
export DB_USER="postgres"
export DB_PASSWORD="postgres123"
export DB_HOST="postgres-applications"
export DB_PORT="5432"

# Service URLs
export USER_SERVICE_URL="http://localhost:8001"
export JOB_SERVICE_URL="http://localhost:8002"

# Kafka configuration
export KAFKA_BOOTSTRAP_SERVERS="localhost:9092"
export KAFKA_GROUP_ID="application-service-group"

echo "🔧 Environment variables set:"
echo "   JWT_SECRET_KEY: $JWT_SECRET_KEY"
echo "   DEBUG: $DEBUG"
echo "   DB_HOST: $DB_HOST"
echo "   USER_SERVICE_URL: $USER_SERVICE_URL"

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️ Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Virtual environment created and activated"
    
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
fi

# Start the service
echo "🌐 Starting Django server on port 8003..."
python manage.py runserver 0.0.0.0:8003
