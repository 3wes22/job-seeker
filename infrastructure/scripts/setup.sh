#!/bin/bash

echo "Setting up Job Platform development environment..."

# Create virtual environments for each service
services=("user-service" "job-service" "application-service" "search-service" "notification-service" "analytics-service")

for service in "${services[@]}"; do
    echo "Setting up $service..."
    cd backend/$service
    
    # Create virtual environment
    python -m venv venv
    source venv/bin/activate
    
    # Install dependencies
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Create Django project if it doesn't exist
    if [ ! -f manage.py ]; then
        django-admin startproject $service .
    fi
    
    cd ../..
done

echo "Creating Docker network..."
docker network create job-platform-network 2>/dev/null || true

echo "Building Docker images..."
docker-compose build

echo "Starting services..."
docker-compose up -d postgres-users postgres-jobs postgres-applications redis

echo "Waiting for databases to be ready..."
sleep 10

echo "Running migrations..."
docker-compose run --rm user-service python manage.py migrate
docker-compose run --rm job-service python manage.py migrate
docker-compose run --rm application-service python manage.py migrate

echo "Setup complete! You can now start development."
echo "Run 'docker-compose up' to start all services."