#!/bin/bash

# Bash script to test yliveticker locally with Docker
# Usage: ./test-local.sh

echo "========================================"
echo "  YLiveTicker Local Test"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed!"
    echo "Please install Docker from: https://www.docker.com/get-started"
    exit 1
fi

# Check if Docker is running
if ! docker ps &> /dev/null; then
    echo "Error: Docker is not running!"
    echo "Please start Docker and try again."
    exit 1
fi

echo "✓ Docker is installed and running"
echo ""

# Build the Docker image
echo "Building Docker image..."
docker build -t yliveticker .

if [ $? -ne 0 ]; then
    echo "Build failed. Please check the errors above."
    exit 1
fi

echo "✓ Build successful!"
echo ""

# Run the container
echo "Starting yliveticker container..."
echo "Press Ctrl+C to stop"
echo ""
echo "You should see market data streaming below:"
echo "----------------------------------------"

docker run --rm yliveticker

echo ""
echo "Container stopped."
echo ""
echo "To deploy to Easypanel, see: QUICKSTART.md"

