#!/bin/bash

# Start Django migrations
echo "Running Django migrations..."
python manage.py migrate

# Start Kafka consumer in background
echo "Starting Kafka consumer in background..."
python manage.py start_kafka_consumer &

# Start Django server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000
