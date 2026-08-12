#!/bin/bash
set -e

echo "Waiting for PostgreSQL to start..."
until pg_isready -h db -p 5432 -U vincentnguyen; do
  sleep 1
done
echo "PostgreSQL is up and running!"

# Optional: Check if data is already loaded, otherwise run ETL and training
echo "Running data ingestion..."
python3 ingest_data.py

echo "Training machine learning pipeline..."
python3 train.py

echo "Starting Flask API server..."
exec python3 app.py