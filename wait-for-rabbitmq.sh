#!/bin/sh

# Wait for RabbitMQ to be healthy
echo "Waiting for RabbitMQ to be healthy..."
sleep 10

# Start the main application
exec "$@"