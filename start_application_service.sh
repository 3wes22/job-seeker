#!/bin/bash

# Simple Application Service Startup Script
echo "🚀 Starting Application Service..."

# Navigate to application service directory
cd backend/application-service

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Set environment variables
export JWT_SECRET_KEY="django-insecure-jwt-secret-key-shared-across-services"
export DEBUG="True"
export SECRET_KEY="django-insecure-jwt-secret-key-shared-across-services"
export DB_NAME="applications_db"
export DB_USER="postgres"
export DB_PASSWORD="postgres123"
export DB_HOST="postgres-applications"
export DB_PORT="5432"
export USER_SERVICE_URL="http://localhost:8001"
export JOB_SERVICE_URL="http://localhost:8002"

echo "🔧 Environment variables set"
echo "🌐 Starting Django server on port 8003..."

# Start Django
python manage.py runserver 0.0.0.0:8003
