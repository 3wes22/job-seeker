#!/bin/bash

# Development Setup Script for Job Platform
# This script sets up the entire development environment

set -e  # Exit on any error

echo "🚀 Setting up Job Platform Development Environment"
echo "=================================================="

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

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi

    print_status "Docker and Docker Compose are installed"
}

# Check if Flutter is installed
check_flutter() {
    if ! command -v flutter &> /dev/null; then
        print_warning "Flutter is not installed. Please install Flutter for mobile development."
        print_info "Download from: https://flutter.dev/docs/get-started/install"
    else
        print_status "Flutter is installed"
        flutter --version
    fi
}

# Check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3."
        exit 1
    fi

    print_status "Python 3 is installed"
}

# Create necessary directories
create_directories() {
    print_info "Creating necessary directories..."
    
    directories=(
        "backend/shared/dummy_data"
        "logs"
        "data/postgres"
        "data/redis"
    )

    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
        print_status "Created directory: $dir"
    done
}

# Generate dummy data
generate_dummy_data() {
    print_info "Generating dummy data..."
    
    if [ -f "backend/shared/dummy_data.py" ]; then
        cd backend/shared
        python3 dummy_data.py
        cd ../..
        print_status "Dummy data generated successfully"
    else
        print_warning "Dummy data generator not found. Skipping dummy data generation."
    fi
}

# Setup backend environment
setup_backend() {
    print_info "Setting up backend services..."
    
    # Create virtual environment for each service
    backend_services=(
        "user-service"
        "job-service"
        "application-service"
        "search-service"
        "notification-service"
        "analytics-service"
    )

    for service in "${backend_services[@]}"; do
        if [ -d "backend/$service" ]; then
            print_info "Setting up $service..."
            cd "backend/$service"
            
            # Create virtual environment if it doesn't exist
            if [ ! -d "venv" ]; then
                python3 -m venv venv
                print_status "Created virtual environment for $service"
            fi
            
            # Activate virtual environment and install dependencies
            source venv/bin/activate
            if [ -f "requirements.txt" ]; then
                print_info "Installing dependencies for $service (this may take a moment)..."
                pip install -r requirements.txt --quiet --no-warn-script-location 2>/dev/null
                if [ $? -eq 0 ]; then
                    print_status "Installed dependencies for $service"
                else
                    print_warning "Some dependencies for $service may have installation issues, but continuing..."
                fi
            fi
            deactivate
            
            cd ../..
        else
            print_warning "Service directory not found: backend/$service"
        fi
    done
}

# Setup Flutter frontend
setup_flutter() {
    if command -v flutter &> /dev/null; then
        print_info "Setting up Flutter frontend..."
        
        cd frontend/flutter-app
        
        # Get Flutter dependencies
        flutter pub get
        print_status "Flutter dependencies installed"
        
        # Run code generation if needed
        if grep -q "build_runner" pubspec.yaml; then
            flutter packages pub run build_runner build --delete-conflicting-outputs
            print_status "Code generation completed"
        fi
        
        cd ../..
    else
        print_warning "Flutter not installed. Skipping Flutter setup."
    fi
}

# Create docker-compose.yml if it doesn't exist
create_docker_compose() {
    if [ ! -f "docker-compose.yml" ]; then
        print_info "Creating docker-compose.yml..."
        
        cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: job_platform
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Redis Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - ./data/redis:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # API Gateway
  api-gateway:
    build:
      context: ./infrastructure/docker/api-gateway
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    depends_on:
      - user-service
      - job-service
      - application-service
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # User Service
  user-service:
    image: python:3.11-slim
    working_dir: /app
    command: bash -c "cd /app && python manage.py runserver 0.0.0.0:8001"
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/job_platform
      - REDIS_URL=redis://redis:6379
      - DJANGO_SETTINGS_MODULE=user_service.settings
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend/user-service:/app
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health/"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Job Service
  job-service:
    image: python:3.11-slim
    working_dir: /app
    command: bash -c "cd /app && python manage.py runserver 0.0.0.0:8002"
    ports:
      - "8002:8002"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/job_platform
      - REDIS_URL=redis://redis:6379
      - DJANGO_SETTINGS_MODULE=job_service.settings
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend/job-service:/app

  # Application Service
  application-service:
    image: python:3.11-slim
    working_dir: /app
    command: bash -c "cd /app && python manage.py runserver 0.0.0.0:8003"
    ports:
      - "8003:8003"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/job_platform
      - REDIS_URL=redis://redis:6379
      - DJANGO_SETTINGS_MODULE=application_service.settings
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend/application-service:/app

  # Search Service
  search-service:
    image: python:3.11-slim
    working_dir: /app
    command: bash -c "cd /app && python manage.py runserver 0.0.0.0:8004"
    ports:
      - "8004:8004"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/job_platform
      - REDIS_URL=redis://redis:6379
      - DJANGO_SETTINGS_MODULE=search_service.settings
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend/search-service:/app

  # Notification Service
  notification-service:
    image: python:3.11-slim
    working_dir: /app
    command: bash -c "cd /app && python manage.py runserver 0.0.0.0:8005"
    ports:
      - "8005:8005"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/job_platform
      - REDIS_URL=redis://redis:6379
      - DJANGO_SETTINGS_MODULE=notification_service.settings
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend/notification-service:/app

  # Analytics Service
  analytics-service:
    image: python:3.11-slim
    working_dir: /app
    command: bash -c "cd /app && python manage.py runserver 0.0.0.0:8006"
    ports:
      - "8006:8006"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/job_platform
      - REDIS_URL=redis://redis:6379
      - DJANGO_SETTINGS_MODULE=analytics_service.settings
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend/analytics-service:/app

volumes:
  postgres_data:
  redis_data:

networks:
  default:
    name: job_platform_network
EOF
        
        print_status "Created docker-compose.yml"
    else
        print_status "docker-compose.yml already exists"
    fi
}

# Start services
start_services() {
    print_info "Starting services with Docker Compose..."
    
    # Build and start services
    docker-compose up -d postgres redis
    print_status "Database services started"
    
    # Wait for databases to be ready
    print_info "Waiting for databases to be ready..."
    sleep 10
    
    # Start backend services
    docker-compose up -d
    print_status "All services started"
    
    # Show service status
    print_info "Service status:"
    docker-compose ps
}

# Load dummy data
load_dummy_data() {
    print_info "Waiting for services to be fully ready..."
    sleep 30
    
    print_info "Loading dummy data..."
    if [ -f "scripts/load_dummy_data.py" ]; then
        python3 scripts/load_dummy_data.py
        print_status "Dummy data loaded successfully"
    else
        print_warning "Dummy data loader not found. Skipping data loading."
    fi
}

# Show helpful information
show_info() {
    echo ""
    print_status "🎉 Development environment setup complete!"
    echo ""
    print_info "Services are running at:"
    echo "  • API Gateway:          http://localhost:8000"
    echo "  • User Service:         http://localhost:8001"
    echo "  • Job Service:          http://localhost:8002"
    echo "  • Application Service:  http://localhost:8003"
    echo "  • Search Service:       http://localhost:8004"
    echo "  • Notification Service: http://localhost:8005"
    echo "  • Analytics Service:    http://localhost:8006"
    echo "  • PostgreSQL:           localhost:5432"
    echo "  • Redis:                localhost:6379"
    echo ""
    print_info "Useful commands:"
    echo "  • View logs:        docker-compose logs -f [service-name]"
    echo "  • Stop services:    docker-compose down"
    echo "  • Restart service:  docker-compose restart [service-name]"
    echo "  • Flutter run:      cd frontend/flutter-app && flutter run"
    echo ""
    print_info "API Documentation available at each service's /docs/ endpoint"
}

# Parse command line arguments
case "${1:-setup}" in
    "setup")
        print_info "Running full setup..."
        check_docker
        check_flutter
        check_python
        create_directories
        generate_dummy_data
        
        # Ask user if they want to skip backend setup for faster start
        print_info "Backend setup can take several minutes. Skip backend dependency installation? (y/N)"
        print_info "Note: You can run './scripts/setup_development.sh backend' later to install dependencies"
        read -r -t 10 skip_backend || skip_backend="N"
        
        if [[ ! "$skip_backend" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            setup_backend
        else
            print_warning "Skipped backend setup. Services may not work until dependencies are installed."
        fi
        
        setup_flutter
        create_docker_compose
        start_services
        load_dummy_data
        show_info
        ;;
    "backend")
        print_info "Setting up backend services only..."
        setup_backend
        print_status "Backend setup completed!"
        ;;
    "start")
        print_info "Starting services..."
        docker-compose up -d
        show_info
        ;;
    "stop")
        print_info "Stopping services..."
        docker-compose down
        print_status "Services stopped"
        ;;
    "restart")
        print_info "Restarting services..."
        docker-compose restart
        print_status "Services restarted"
        ;;
    "logs")
        if [ -n "$2" ]; then
            docker-compose logs -f "$2"
        else
            docker-compose logs -f
        fi
        ;;
    "clean")
        print_warning "This will remove all containers, volumes, and data. Are you sure? (y/N)"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            docker-compose down -v --remove-orphans
            docker system prune -f
            rm -rf data/
            print_status "Environment cleaned"
        else
            print_info "Clean operation cancelled"
        fi
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  setup     - Full development environment setup (default)"
        echo "  backend   - Setup backend services dependencies only"
        echo "  start     - Start all services"
        echo "  stop      - Stop all services"
        echo "  restart   - Restart all services"
        echo "  logs      - Show logs (optionally specify service name)"
        echo "  clean     - Remove all containers and data"
        echo "  help      - Show this help message"
        ;;
    *)
        print_error "Unknown command: $1"
        print_info "Run '$0 help' for usage information"
        exit 1
        ;;
esac
