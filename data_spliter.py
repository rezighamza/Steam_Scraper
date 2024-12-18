import pandas as pd

# Read the full CSV
df = pd.read_csv('steam_id.csv')

# Split into chunks of 1,000 rows
chunk_size = 1000
for i in range(0, len(df), chunk_size):
    chunk = df[i:i + chunk_size]
    chunk.to_csv(f'steam_id_chunk_{i // chunk_size + 1}.csv', index=False)
