FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install development dependencies if in development mode
ARG ENVIRONMENT=production
COPY requirements-dev.txt .
RUN if [ "$ENVIRONMENT" = "development" ]; then \
        pip install --no-cache-dir -r requirements-dev.txt; \
    fi

# Copy application code
COPY . .

# Make the startup script executable
RUN chmod +x start_with_kafka.sh

# Expose port
EXPOSE 8000

# Run migrations and start server with Kafka consumer
CMD ["./start_with_kafka.sh"]
