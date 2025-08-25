#!/bin/bash

# Kafka Integration Setup Script for Job Platform
# This script sets up the complete Kafka integration between microservices

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
KAFKA_BOOTSTRAP_SERVERS="localhost:9092"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}🚀 Kafka Integration Setup for Job Platform${NC}"
echo "=================================================="

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

# Check if Docker is running
check_docker() {
    print_info "Checking Docker status..."
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker Desktop first."
        exit 1
    fi
    print_status "Docker is running"
}

# Start Kafka infrastructure
start_kafka() {
    print_info "Starting Kafka infrastructure..."
    
    cd "$PROJECT_ROOT"
    
    # Start only Kafka-related services
    if docker-compose up -d zookeeper kafka kafka-ui; then
        print_status "Kafka infrastructure started successfully"
        
        # Wait for Kafka to be ready
        print_info "Waiting for Kafka to be ready..."
        sleep 30
        
        # Check if Kafka is responding
        if docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --list > /dev/null 2>&1; then
            print_status "Kafka is ready and responding"
        else
            print_warning "Kafka might not be fully ready yet. Continuing anyway..."
        fi
    else
        print_error "Failed to start Kafka infrastructure"
        exit 1
    fi
}

# Setup Kafka topics
setup_topics() {
    print_info "Setting up Kafka topics..."
    
    cd "$PROJECT_ROOT"
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 is required but not installed"
        exit 1
    fi
    
    # Install required Python packages if not available
    print_info "Installing required Python packages..."
    pip3 install kafka-python || {
        print_warning "Failed to install kafka-python via pip3, trying pip..."
        pip install kafka-python || {
            print_error "Failed to install kafka-python. Please install it manually:"
            print_error "pip install kafka-python"
            exit 1
        }
    }
    
    # Run topic setup script
    if python3 scripts/setup_kafka_topics.py --bootstrap-servers "$KAFKA_BOOTSTRAP_SERVERS"; then
        print_status "Kafka topics created successfully"
    else
        print_error "Failed to create Kafka topics"
        exit 1
    fi
}

# Test Kafka integration
test_integration() {
    print_info "Testing Kafka integration..."
    
    cd "$PROJECT_ROOT"
    
    if python3 scripts/test_kafka_integration.py --bootstrap-servers "$KAFKA_BOOTSTRAP_SERVERS"; then
        print_status "Kafka integration test passed"
    else
        print_warning "Kafka integration test failed. This might be expected if services aren't running yet."
    fi
}

# Setup backend services
setup_backend() {
    print_info "Setting up backend services for Kafka integration..."
    
    cd "$PROJECT_ROOT"
    
    # Check if setup script exists
    if [ -f "scripts/setup_development.sh" ]; then
        print_info "Running backend setup script..."
        if ./scripts/setup_development.sh backend; then
            print_status "Backend services setup completed"
        else
            print_warning "Backend setup had some issues, but continuing..."
        fi
    else
        print_warning "Backend setup script not found, skipping..."
    fi
}

# Start backend services
start_backend() {
    print_info "Starting backend services..."
    
    cd "$PROJECT_ROOT"
    
    # Start all services
    if docker-compose up -d; then
        print_status "All services started successfully"
        
        # Wait for services to be ready
        print_info "Waiting for services to be ready..."
        sleep 20
        
        # Check service status
        print_info "Checking service status..."
        docker-compose ps
        
    else
        print_error "Failed to start some services"
        print_info "You can check individual service logs with: docker-compose logs [service-name]"
    fi
}

# Start Kafka consumers
start_consumers() {
    print_info "Starting Kafka consumers..."
    
    cd "$PROJECT_ROOT"
    
    # Start user service consumer in background
    print_info "Starting User Service Kafka consumer..."
    cd backend/user-service
    python3 manage.py start_kafka_consumer &
    USER_CONSUMER_PID=$!
    echo $USER_CONSUMER_PID > .user_consumer.pid
    cd "$PROJECT_ROOT"
    
    # Start job service consumer in background
    print_info "Starting Job Service Kafka consumer..."
    cd backend/job-service
    python3 manage.py start_kafka_consumer &
    JOB_CONSUMER_PID=$!
    echo $JOB_CONSUMER_PID > .job_consumer.pid
    cd "$PROJECT_ROOT"
    
    print_status "Kafka consumers started (PIDs: $USER_CONSUMER_PID, $JOB_CONSUMER_PID)"
    print_info "Consumer logs will be written to their respective service log files"
}

# Show next steps
show_next_steps() {
    echo ""
    echo -e "${BLUE}🎉 Kafka Integration Setup Complete!${NC}"
    echo "=============================================="
    echo ""
    echo -e "${GREEN}What's been set up:${NC}"
    echo "✓ Kafka cluster with Zookeeper"
    echo "✓ Kafka UI at http://localhost:8080"
    echo "✓ All required Kafka topics"
    echo "✓ User and Job service event publishers"
    echo "✓ Event consumers for cross-service communication"
    echo "✓ Management commands for starting consumers"
    echo ""
    echo -e "${GREEN}Next steps:${NC}"
    echo "1. View Kafka UI: http://localhost:8080"
    echo "2. Test the integration: ./scripts/test_kafka_integration.py"
    echo "3. Start Flutter app: cd frontend/flutter-app && flutter run"
    echo "4. Monitor events in real-time via Kafka UI"
    echo ""
    echo -e "${GREEN}Useful commands:${NC}"
    echo "• View service logs: docker-compose logs -f [service-name]"
    echo "• Stop all services: docker-compose down"
    echo "• Restart services: docker-compose restart"
    echo "• Check consumer status: ps aux | grep start_kafka_consumer"
    echo ""
    echo -e "${GREEN}Monitoring:${NC}"
    echo "• Kafka UI: http://localhost:8080"
    echo "• Service logs: docker-compose logs -f"
    echo "• Consumer logs: Check .user_consumer.pid and .job_consumer.pid files"
}

# Main execution
main() {
    echo "Starting Kafka integration setup..."
    echo ""
    
    # Check prerequisites
    check_docker
    
    # Start Kafka infrastructure
    start_kafka
    
    # Setup topics
    setup_topics
    
    # Test basic integration
    test_integration
    
    # Setup backend services
    setup_backend
    
    # Start backend services
    start_backend
    
    # Start Kafka consumers
    start_consumers
    
    # Show next steps
    show_next_steps
}

# Handle script interruption
trap 'echo -e "\n${YELLOW}Setup interrupted. Cleaning up...${NC}"; exit 1' INT TERM

# Run main function
main "$@"
