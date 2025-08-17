#!/bin/bash

echo "🚀 Starting minimal backend services for Flutter app..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start PostgreSQL database
echo "📦 Starting PostgreSQL database..."
docker-compose -f docker-compose.minimal.yml up -d postgres redis

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Start User Service
echo "👤 Starting User Service..."
cd backend/user-service

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment for user service..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Start the service
echo "🚀 Starting User Service on port 8001..."
python manage.py runserver 0.0.0.0:8001 &

# Store the PID
USER_SERVICE_PID=$!
echo $USER_SERVICE_PID > .user_service.pid

echo ""
echo "✅ Minimal backend services started!"
echo "📱 Your Flutter app can now connect to:"
echo "   - User Service: http://localhost:8001"
echo ""
echo "🛑 To stop services, run: ./scripts/stop_minimal_backend.sh"
echo "📊 To check service status, run: ./scripts/check_minimal_backend.sh"
