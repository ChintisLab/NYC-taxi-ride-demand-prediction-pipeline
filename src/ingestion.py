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

if __name__ == "__main__":
    # Test with Jan 2024 data
    fetch_taxi_data(2024, 1)
