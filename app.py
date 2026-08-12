import os
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
import joblib
import pandas as pd

app = Flask(__name__)

print("Loading ML model pipeline...")
model = joblib.load('dc_model.pkl')

db_uri = os.environ.get('DATABASE_URL', "postgresql://vincentnguyen@localhost:5432/dc_housing_db")
engine = create_engine(db_uri)

@app.route('/predict', methods=['POST'])
def predict_price():
    data = request.json
    
    # 1. Extract all features, including our new categorical ones
    features = {
        'bathrm': data.get('bathrm'),
        'rooms': data.get('rooms'),
        'bedrm': data.get('bedrm'),
        'ayb': data.get('ayb'),
        'grade': data.get('grade'),
        'style': data.get('style'),
        'cndtn': data.get('cndtn')
    }
    
    input_df = pd.DataFrame([features])
    
    # The pipeline automatically handles One-Hot Encoding and scaling!
    prediction = model.predict(input_df)[0]
    
    # 2. Update logging to store the new metadata
    with engine.connect() as conn:
        query = text("""
            INSERT INTO prediction_logs 
            (input_bathrm, input_rooms, input_bedrm, input_ayb, predicted_price)
            VALUES (:bathrm, :rooms, :bedrm, :ayb, :price)
        """)
        conn.execute(query, {
            'bathrm': features['bathrm'],
            'rooms': features['rooms'],
            'bedrm': features['bedrm'],
            'ayb': features['ayb'],
            'price': float(prediction)
        })
        conn.commit()
        
    return jsonify({
        "status": "success",
        "features_used": features,
        "estimated_price": round(prediction, 2)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)