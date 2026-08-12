import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import joblib

engine = create_engine("postgresql://vincentnguyen@localhost:5432/dc_housing_db")

print("1. Querying data from PostgreSQL (this may take a few seconds)...")
query = "SELECT bathrm, rooms, bedrm, ayb, grade, style, cndtn, price FROM historical_homes"

# Read the database in chunks to prevent memory spikes
chunks = []
chunksize = 25000
for chunk in pd.read_sql(query, engine, chunksize=chunksize):
    chunks.append(chunk)
    print(f" Loaded {sum(len(c) for c in chunks):,} rows...")

df = pd.concat(chunks, ignore_index=True)
print(f"Total dataset size: {len(df):,} rows.")

# Drop nulls
df = df.dropna()

X = df[['bathrm', 'rooms', 'bedrm', 'ayb', 'grade', 'style', 'cndtn']]
y = df['price']

# 2. Define the Preprocessing Steps
numeric_features = ['bathrm', 'rooms', 'bedrm', 'ayb']
numeric_transformer = StandardScaler()

categorical_features = ['grade', 'style', 'cndtn']
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# 3. Create and Train the Pipeline
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)) 
    # Note: n_jobs=-1 tells Random Forest to use ALL your Mac's CPU cores to train faster!
])

print("3. Training the Random Forest model across all CPU cores...")
model_pipeline.fit(X, y)
print("Training complete!")

print("4. Serializing the model...")
joblib.dump(model_pipeline, 'dc_model.pkl')
print("Pipeline successfully saved to dc_model.pkl!")