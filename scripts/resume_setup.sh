#!/bin/bash

# Resume Setup Script - Continue from where setup was interrupted
# This script handles the setup process that was suspended

set -e  # Exit on any error

echo "🔄 Resuming Job Platform Setup"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Kill any suspended processes
print_info "Cleaning up any suspended processes..."
jobs -p | xargs -r kill 2>/dev/null || true

# Check if we need to continue the backend setup
if [ -d "backend/notification-service/venv" ] && [ -d "backend/analytics-service/venv" ]; then
    print_status "Backend services already set up"
else
    print_info "Continuing backend setup..."
    ./scripts/setup_development.sh backend
fi

# Check if Flutter setup is needed
if command -v flutter &> /dev/null; then
    print_info "Setting up Flutter frontend..."
    cd frontend/flutter-app
    flutter pub get
    print_status "Flutter dependencies installed"
    cd ../..
else
    print_warning "Flutter not installed. Skipping Flutter setup."
fi

# Create docker-compose.yml if it doesn't exist
if [ ! -f "docker-compose.yml" ]; then
    print_info "Creating docker-compose.yml..."
    ./scripts/setup_development.sh help > /dev/null 2>&1  # This will create the file
    print_status "Docker Compose configuration created"
fi

# Start services
print_info "Starting services with Docker Compose..."
docker-compose up -d postgres redis
print_status "Database services started"

# Wait for databases
print_info "Waiting for databases to be ready..."
sleep 10

# Skip the Django services for now since they need dependencies
print_info "Starting basic services only (you can start Django services manually later)..."

# Show status
print_info "Service status:"
docker-compose ps

# Show helpful information
print_status "🎉 Setup resumed successfully!"
echo ""
print_info "Next steps:"
echo "  1. Install backend dependencies (if not done): ./scripts/setup_development.sh backend"
echo "  2. Start Django services: docker-compose up -d"
echo "  3. Run Flutter app: cd frontend/flutter-app && flutter run"
echo ""
print_info "Quick commands:"
echo "  • Start all services:   docker-compose up -d"
echo "  • View logs:           docker-compose logs -f [service-name]"
echo "  • Stop services:       docker-compose down"
echo ""
print_info "Services will be available at:"
echo "  • API Gateway:          http://localhost:8000"
echo "  • User Service:         http://localhost:8001"
echo "  • Job Service:          http://localhost:8002"
echo "  • PostgreSQL:           localhost:5432"
echo "  • Redis:                localhost:6379"
