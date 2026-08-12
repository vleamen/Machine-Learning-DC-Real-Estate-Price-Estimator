import os
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
import joblib
import pandas as pd

app = Flask(__name__)

print("Loading ML model pipeline...")
model = joblib.load('dc_model.pkl')

db_uri = os.environ.get('DATABASE_URL', "postgresql://vincentnguyen:password@db:5432/dc_housing_db")
engine = create_engine(db_uri)

@app.route('/predict', methods=['POST'])
def predict_price():
    data = request.json
    
    # 1. Format the features (zipcode removed)
    features = pd.DataFrame([{
        'bathrm': data['bathrm'],
        'rooms': data['rooms'],
        'bedrm': data['bedrm'],
        'ayb': data['ayb'],
        'grade': data['grade'],
        'style': data['style'],
        'cndtn': data['cndtn'],
        'gba': data['gba']
    }])

    prediction = model.predict(features)

    # 2. Update logging (zipcode removed from SQL)
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS prediction_logs (
                    id SERIAL PRIMARY KEY,
                    input_bathrm INT,
                    input_rooms INT,
                    input_bedrm INT,
                    input_ayb INT,
                    input_gba FLOAT,
                    predicted_price FLOAT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()

            query = text("""
                INSERT INTO prediction_logs 
                (input_bathrm, input_rooms, input_bedrm, input_ayb, input_gba, predicted_price)
                VALUES (:bathrm, :rooms, :bedrm, :ayb, :gba, :price)
            """)
            conn.execute(query, {
                'bathrm': int(data['bathrm']),
                'rooms': int(data['rooms']),
                'bedrm': int(data['bedrm']),
                'ayb': int(data['ayb']),
                'gba': float(data['gba']),
                'price': float(prediction[0])
            })
            conn.commit()
    except Exception as e:
        print(f"Logging warning: Could not save to audit table: {e}")

    return jsonify({'estimated_price': float(prediction[0])})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)