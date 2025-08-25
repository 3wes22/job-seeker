#!/bin/bash

# Development Environment Setup Script for Job Platform
# This script sets up the development environment with all necessary tools

set -e

echo "🚀 Setting up Job Platform Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3.11+ is required but not installed"
        exit 1
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is required but not installed"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is required but not installed"
        exit 1
    fi
    
    # Check Flutter
    if ! command -v flutter &> /dev/null; then
        print_warning "Flutter is not installed. Please install Flutter for mobile development."
    fi
    
    print_success "System requirements check passed"
}

# Setup Python virtual environments
setup_python_envs() {
    print_status "Setting up Python virtual environments..."
    
    # User Service
    if [ ! -d "backend/user-service/venv" ]; then
        print_status "Creating virtual environment for user-service..."
        cd backend/user-service
        python3 -m venv venv
        cd ../..
    fi
    
    # Job Service
    if [ ! -d "backend/job-service/venv" ]; then
        print_status "Creating virtual environment for job-service..."
        cd backend/job-service
        python3 -m venv venv
        cd ../..
    fi
    
    print_success "Python virtual environments created"
}

# Install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    # User Service
    print_status "Installing user-service dependencies..."
    cd backend/user-service
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    cd ../..
    
    # Job Service
    print_status "Installing job-service dependencies..."
    cd backend/job-service
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    cd ../..
    
    print_success "Python dependencies installed"
}

# Setup pre-commit hooks
setup_precommit() {
    print_status "Setting up pre-commit hooks..."
    
    if command -v pre-commit &> /dev/null; then
        pre-commit install
        pre-commit install --hook-type commit-msg
        print_success "Pre-commit hooks installed"
    else
        print_warning "pre-commit not installed. Installing now..."
        pip install pre-commit
        pre-commit install
        pre-commit install --hook-type commit-msg
        print_success "Pre-commit hooks installed"
    fi
}

# Setup Flutter dependencies
setup_flutter() {
    if command -v flutter &> /dev/null; then
        print_status "Setting up Flutter dependencies..."
        cd frontend/flutter-app
        flutter pub get
        flutter pub run build_runner build --delete-conflicting-outputs
        cd ../..
        print_success "Flutter dependencies installed"
    else
        print_warning "Flutter not available, skipping Flutter setup"
    fi
}

# Create development environment file
create_env_file() {
    print_status "Creating development environment file..."
    
    if [ ! -f ".env.development" ]; then
        cat > .env.development << EOF
# Development Environment Configuration
DEBUG=True
ENVIRONMENT=development

# Database URLs
DATABASE_URL=postgresql://postgres:postgres123@localhost:5438/job_platform_dev
USER_SERVICE_DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/users_db
JOB_SERVICE_DATABASE_URL=postgresql://postgres:postgres123@localhost:5433/jobs_db

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_GROUP_ID=dev-group

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Service URLs
USER_SERVICE_URL=http://localhost:8001
JOB_SERVICE_URL=http://localhost:8002

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here-change-in-production
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# Logging
LOG_LEVEL=DEBUG
EOF
        print_success "Development environment file created"
    else
        print_status "Development environment file already exists"
    fi
}

# Setup monitoring directories
setup_monitoring() {
    print_status "Setting up monitoring directories..."
    
    mkdir -p monitoring/prometheus
    mkdir -p monitoring/grafana/dashboards
    mkdir -p monitoring/grafana/datasources
    
    # Create basic Prometheus config
    if [ ! -f "monitoring/prometheus.yml" ]; then
        cat > monitoring/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'user-service'
    static_configs:
      - targets: ['user-service:8000']
    metrics_path: '/metrics/'

  - job_name: 'job-service'
    static_configs:
      - targets: ['job-service:8000']
    metrics_path: '/metrics/'
EOF
        print_success "Prometheus configuration created"
    fi
    
    # Create basic Grafana datasource
    if [ ! -f "monitoring/grafana/datasources/prometheus.yml" ]; then
        cat > monitoring/grafana/datasources/prometheus.yml << EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF
        print_success "Grafana datasource configuration created"
    fi
}

# Main setup function
main() {
    print_status "Starting development environment setup..."
    
    check_requirements
    setup_python_envs
    install_python_deps
    setup_precommit
    setup_flutter
    create_env_file
    setup_monitoring
    
    print_success "Development environment setup completed!"
    echo ""
    echo "Next steps:"
    echo "1. Copy .env.development to .env and customize values"
    echo "2. Start services: docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d"
    echo "3. Run migrations: ./scripts/run_migrations.sh"
    echo "4. Start development servers: ./scripts/start_dev_servers.sh"
    echo ""
    echo "Happy coding! 🎉"
}

# Run main function
main "$@"
