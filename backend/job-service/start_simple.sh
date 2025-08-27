#!/bin/bash

# Start Django migrations
echo "Running Django migrations..."
python manage.py migrate

# Start Django server without Kafka
echo "Starting Django server without Kafka..."
python manage.py runserver 0.0.0.0:8000
