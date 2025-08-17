#!/bin/bash

echo "📊 Checking minimal backend services status..."
echo ""

# Check PostgreSQL
echo "🗄️ PostgreSQL Database:"
if docker ps | grep -q "postgres"; then
    echo "   ✅ Running"
    echo "   📍 Port: 5432"
else
    echo "   ❌ Not running"
fi

echo ""

# Check User Service
echo "👤 User Service:"
if [ -f "backend/user-service/.user_service.pid" ]; then
    USER_SERVICE_PID=$(cat backend/user-service/.user_service.pid)
    if ps -p $USER_SERVICE_PID > /dev/null; then
        echo "   ✅ Running (PID: $USER_SERVICE_PID)"
        echo "   📍 Port: 8001"
        echo "   🌐 URL: http://localhost:8001"
    else
        echo "   ❌ PID file exists but process not running"
        rm backend/user-service/.user_service.pid
    fi
else
    echo "   ❌ Not running"
fi

echo ""

# Check if services are responding
echo "🔍 Service Health Check:"
if curl -s http://localhost:8001/admin/ > /dev/null 2>&1; then
    echo "   ✅ User Service responding"
else
    echo "   ❌ User Service not responding"
fi

echo ""
echo "📱 Flutter App Configuration:"
echo "   - User Service URL: http://10.0.2.2:8001 (Android Emulator)"
echo "   - User Service URL: http://localhost:8001 (iOS Simulator)"
echo "   - User Service URL: http://localhost:8001 (Web)"
