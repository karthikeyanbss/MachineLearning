#!/bin/bash
# Script to build and run Docker container

echo "Building Docker image..."
docker build -t ner-service:latest .

echo "Running Docker container..."
docker run -d \
  --name ner-service \
  -p 8000:8000 \
  --env-file config/.env.example \
  ner-service:latest

echo "NER Service is running at http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "To stop the service: docker stop ner-service"
echo "To remove the container: docker rm ner-service"
