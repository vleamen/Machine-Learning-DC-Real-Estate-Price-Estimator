# DC Real Estate Price Estimator

An end-to-end machine learning pipeline and REST API that predicts residential property prices in Washington, D.C. using historical assessment data from the city's CAMA database.

This project demonstrates a production-grade decoupled architecture: raw property data is ingested into a PostgreSQL database, processed and trained via a scikit-learn pipeline, served through a Flask web application, tracked using request logging for model monitoring, and fully containerized for one-command deployment.

## Architecture & Tech Stack
Machine Learning: scikit-learn (Random Forest Regressor, Pipelines, ColumnTransformers, OneHotEncoder, StandardScaler)

Backend / API: Flask, SQLAlchemy, psycopg2

Database: PostgreSQL

Containerization: Docker, Docker Compose, Bash

## Pipeline Overview
Ingestion (ingest_data.py): Parses raw property assessment records from the D.C. CSV dataset, filters for recent transactions (2020 and newer) to reflect modern market conditions, extracts key valuation features including Gross Building Area (gba), and bulk-inserts them into PostgreSQL.

Feature Engineering & Training (train.py): Streams data out of Postgres in chunks to optimize memory, standardizes numerical features (bathrm, rooms, bedrm, ayb, gba), one-hot encodes high-impact categorical features (grade, style, cndtn), and trains a multi-core optimized Random Forest model bundled inside a scikit-learn Pipeline.

Serving & Auditing (app.py): Loads the serialized .pkl artifact into memory on startup, accepts property JSON payloads, generates real-time predictions, and logs every incoming request and estimated price to a Postgres audit table.

## Data Limitations & The Location Disparity
Real estate valuation is heavily dependent on location. However, this model currently outputs a city-wide average for a property based strictly on its physical and structural attributes.

The High Cardinality Problem:
In the dataset utilized for this build, broad geographic identifiers (such as ZIPCODE or WARD) were unavailable. The only location metric provided was SSL (Square, Suffix, Lot)—a highly granular tax identifier unique to almost every individual parcel of land.

Feeding SSL into a One-Hot Encoder would generate tens of thousands of binary columns, creating a "high cardinality" problem that leads to severe model overfitting and memory exhaustion. Consequently, location data was intentionally excluded from the training pipeline.

As a result, the API will output the exact same baseline valuation for an 1,800 sq. ft., 3-bedroom rowhouse regardless of whether it is located in Capitol Hill or Anacostia. Future iterations of this project could involve integrating an external GIS crosswalk to map SSL coordinates to broader Wards, allowing the model to weigh neighborhood market disparities accurately.

## Project Structure
├── app.py              # Flask REST API server and database logger
├── ingest_data.py      # ETL script to parse CSV and load into PostgreSQL
├── train.py            # Feature engineering and model training script
├── entrypoint.sh       # Container orchestration script (waits for DB, runs ETL & training)
├── start.sh            # Master developer startup script
├── Dockerfile          # Multi-stage image build configuration
├── docker-compose.yml  # Local multi-container orchestration
├── requirements.txt    # Pinned Python dependencies
└── README.md           # Project documentation
## Quick Start
To run the entire ecosystem (PostgreSQL database, automated data ingestion, model training, and the Flask API) inside isolated containers, ensure you have Docker Desktop installed and running, then execute:

./start.sh

The script will automatically build the containers, ingest the dataset, train the model, and spin up the API server.
(Note: The first execution may take a moment while the Random Forest processes the training dataset).

## API Usage
Once the container is running, send a POST request to the prediction endpoint with the property specifications:

Example Request:

curl -X POST http://127.0.0.1:5001/predict \
     -H "Content-Type: application/json" \
     -d '{
           "bathrm": 2, 
           "rooms": 6, 
           "bedrm": 3, 
           "ayb": 1950, 
           "grade": "Average", 
           "style": "2 Story", 
           "cndtn": "Good",
           "gba": 1800
         }'

Example Response:

JSON
{
  "estimated_price_formatted": "$369,357.71",
  "estimated_price_raw": 369357.70666666667
}

## Manual Management Commands

View Live Logs:

docker-compose logs -f

Stop the Application:

docker-compose down