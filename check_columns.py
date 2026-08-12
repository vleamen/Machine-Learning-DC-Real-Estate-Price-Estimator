import pandas as pd

# nrows=0 loads just the headers, making this instant
df = pd.read_csv('DC_Properties.csv', nrows=0)
print(df.columns.tolist())