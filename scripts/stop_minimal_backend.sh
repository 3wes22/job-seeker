#!/bin/bash

echo "🛑 Stopping minimal backend services..."

# Stop User Service
if [ -f "backend/user-service/.user_service.pid" ]; then
    USER_SERVICE_PID=$(cat backend/user-service/.user_service.pid)
    echo "🛑 Stopping User Service (PID: $USER_SERVICE_PID)..."
    kill $USER_SERVICE_PID 2>/dev/null || true
    rm backend/user-service/.user_service.pid
else
    echo "🔍 User Service PID file not found, stopping by process name..."
    pkill -f "manage.py runserver.*8001" 2>/dev/null || true
fi

# Stop PostgreSQL and Redis
echo "🛑 Stopping PostgreSQL and Redis..."
docker-compose -f docker-compose.minimal.yml down

echo "✅ All minimal backend services stopped!"
