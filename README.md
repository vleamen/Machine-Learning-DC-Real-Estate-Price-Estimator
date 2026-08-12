# DC Real Estate Price Estimator

An end-to-end machine learning pipeline and REST API that predicts residential property prices in Washington, D.C. using historical assessment data from the city's CAMA database. 

This project demonstrates a production-grade decoupled architecture: raw property data is ingested into a PostgreSQL database, processed and trained via a scikit-learn pipeline, served through a Flask web application, tracked using request logging for model monitoring, and fully containerized for one-command deployment.

## Architecture & Tech Stack

- **Machine Learning:** `scikit-learn` (Random Forest Regressor, Pipelines, ColumnTransformers, OneHotEncoder, StandardScaler)
- **Backend / API:** `Flask`, `SQLAlchemy`, `psycopg2`
- **Database:** `PostgreSQL`
- **Containerization:** `Docker`, `Docker Compose`, `Bash`

## Pipeline Overview

1. **Ingestion (`ingest_data.py`):** Parses raw property assessment records from the D.C. CSV dataset, extracts key valuation features, and bulk-inserts them into PostgreSQL.
2. **Feature Engineering & Training (`train.py`):** Streams data out of Postgres in chunks, standardizes numerical features (`bathrm`, `rooms`, `bedrm`, `ayb`), one-hot encodes high-impact categorical features (`grade`, `style`, `cndtn`), and trains a multi-core optimized Random Forest model bundled inside a scikit-learn `Pipeline`.
3. **Serving & Auditing (`app.py`):** Loads the serialized `.pkl` artifact into memory on startup, accepts property JSON payloads, generates real-time predictions, and logs every incoming request and estimated price to a Postgres audit table.

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

Once the container is running, send a POST request to the prediction endpoint with property specifications:

Example Request:

curl -X POST [http://127.0.0.1:5000/predict](http://127.0.0.1:5000/predict) \
     -H "Content-Type: application/json" \
     -d '{
           "bathrm": 2, 
           "rooms": 6, 
           "bedrm": 3, 
           "ayb": 1950, 
           "grade": "Average", 
           "style": "2 Story", 
           "cndtn": "Good"
         }'

Example Response:

{
  "estimated_price": 296838.88,
  "features_used": {
    "ayb": 1950,
    "bathrm": 2,
    "bedrm": 3,
    "cndtn": "Good",
    "grade": "Average",
    "rooms": 6,
    "style": "2 Story"
  },
  "status": "success"
}

## Manual Management Commands

View Live Logs:
docker-compose logs -f

Stop the Application:
docker-compose down