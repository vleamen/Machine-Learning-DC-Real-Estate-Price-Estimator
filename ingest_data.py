import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://vincentnguyen@localhost:5432/dc_housing_db")

print("Reading CSV...")
df = pd.read_csv('DC_Properties.csv', low_memory=False)

# 1. Grab all the new features
cols_to_keep = ['BATHRM', 'ROOMS', 'BEDRM', 'AYB', 'GRADE', 'STYLE', 'CNDTN', 'PRICE']
df_filtered = df[cols_to_keep]

df_filtered = df_filtered.dropna()

# 2. Map them to SQL columns
df_filtered.columns = ['bathrm', 'rooms', 'bedrm', 'ayb', 'grade', 'style', 'cndtn', 'price']

print(f"Inserting {len(df_filtered)} rows into the database...")
df_filtered.to_sql('historical_homes', engine, if_exists='append', index=False)

print("Data successfully loaded!")