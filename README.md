# DC Real Estate Price Estimator

An end-to-end machine learning pipeline and REST API that predicts residential property prices in Washington, D.C. using historical assessment data from the city's CAMA database. 

The project demonstrates a decoupled architecture: raw data is ingested into a PostgreSQL database, processed and trained via a scikit-learn pipeline, served through a Flask web application, and tracked using request logging for model monitoring.

## Architecture & Tech Stack

- **Machine Learning:** `scikit-learn` (Random Forest Regressor, Pipelines, ColumnTransformers, OneHotEncoder, StandardScaler)
- **Backend / API:** `Flask`, `SQLAlchemy`, `psycopg2`
- **Database:** `PostgreSQL`
- **Serialization:** `joblib`

## Pipeline Overview

1. **Infiltration & Ingestion (`ingest_data.py`):** Pulls raw property assessment records from a CSV, filters relevant features, and bulk-inserts them into PostgreSQL.
2. **Feature Engineering & Training (`train.py`):** Queries the database in chunks, standardizes numerical features (`bathrm`, `rooms`, `bedrm`, `ayb`), one-hot encodes high-impact categorical features (`grade`, `style`, `cndtn`), and trains a multi-core optimized Random Forest model bundled inside a scikit-learn `Pipeline`.
3. **Serving & Logging (`app.py`):** Loads the serialized `.pkl` artifact into memory on startup, accepts property JSON payloads, generates real-time predictions, and logs every transaction to a Postgres audit table.

## Project Structure

├── app.py              # Flask REST API server and database logger
├── ingest_data.py      # ETL script to parse CSV and load into PostgreSQL
├── train.py            # Feature engineering and model training script
├── requirements.txt    # Project dependencies
└── dc_model.pkl        # Serialized scikit-learn pipeline artifact (git-ignored or included)


## Getting Started

1. Prerequisites
    Ensure you have Python 3.9+, PostgreSQL installed locally, and your raw DC_Properties.csv file placed in the project directory.

2. Open your terminal and create the local PostgreSQL database:
    createdb dc_housing_db
    
3. Install Dependencies
    pip install -r requirements.txt

4. Execute the ETL script to populate your database:
    python3 ingest_data.py

5. Run the training script to generate the model artifact:
    python3 train.py

6. Start the API Server
    python3 app.py

## API Usage
Send a POST request to the prediction endpoint with property specifications:

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

JSON
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