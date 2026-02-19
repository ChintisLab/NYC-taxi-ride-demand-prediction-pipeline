import requests
import os
from tqdm import tqdm

def download_file(url, target_path):
    if os.path.exists(target_path):
        print(f"File already exists: {target_path}")
        return
    
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(target_path, 'wb') as file, tqdm(
        desc=os.path.basename(target_path),
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

def fetch_taxi_data(year, month, color='yellow'):
    # Example URL: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-{month:02d}.parquet"
    target_path = f"data/raw/{color}/{year}-{month:02d}.parquet"
    download_file(url, target_path)
    return target_path

import duckdb
from src.db import DBConnector

def ingest_to_db(file_path, table_name, db_connector):
    query = f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM read_parquet('{file_path}')"
    db_connector.execute(query)
    print(f"Ingested {file_path} into {table_name}")

if __name__ == "__main__":
    db = DBConnector()
    # Test with Jan 2024 data
    file_path = fetch_taxi_data(2024, 1)
    ingest_to_db(file_path, "raw_yellow_taxi", db)
    db.close()
