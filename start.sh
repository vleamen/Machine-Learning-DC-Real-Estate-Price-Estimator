#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "=================================================="
echo " Starting DC Real Estate ML Pipeline & API..."
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

# Build and start the containers in detached mode (or attached if you want to see logs)
echo "Building and spinning up Docker containers..."
docker-compose up --build -d

echo "=================================================="
echo " Containers are spinning up!"
echo " Note: The first run will take a moment as it ingests"
echo " the CSV data and trains the Random Forest model."
echo "=================================================="
echo ""
echo "To view live logs, run: docker-compose logs -f"
echo "To stop the app, run:   docker-compose down"
echo ""
echo "Once the logs show 'Running on http://127.0.0.1:5000', test it with:"
echo ""
echo 'curl -X POST http://127.0.0.1:5000/predict \'
echo '     -H "Content-Type: application/json" \'
echo "     -d '{"
echo '           "bathrm": 2,'
echo '           "rooms": 6,'
echo '           "bedrm": 3,'
echo '           "ayb": 1950,'
echo '           "grade": "Average",'
echo '           "style": "2 Story",'
echo '           "cndtn": "Good"'
echo "         }'"
echo "=================================================="