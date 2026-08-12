import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://vincentnguyen:password@db:5432/dc_housing_db")

# 1. Read the CSV
df = pd.read_csv('DC_Properties.csv', low_memory=False)
df.columns = df.columns.str.lower()

# 2. Filter for sales from 2020 onward
df['saledate'] = pd.to_datetime(df['saledate'], errors='coerce')
df = df[df['saledate'].dt.year >= 2020]

# 3. Select columns (zipcode removed, gba stays)
columns_to_keep = ['bathrm', 'rooms', 'bedrm', 'ayb', 'grade', 'style', 'cndtn', 'gba', 'price']
df = df[columns_to_keep]

# 4. Clean the data
df = df.dropna()

print(f"Inserting {len(df)} rows into the database...")
df.to_sql('historical_homes', engine, if_exists='replace', index=False)
print("Data successfully loaded!")