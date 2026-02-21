import os
import requests
from tqdm import tqdm
from src.db import DBConnector
from src.logger import get_logger

logger = get_logger(__name__)


def download_file(url, target_path):
    if os.path.exists(target_path):
        logger.info(f"File already exists: {target_path}")
        return

    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    logger.info(f"Starting download: {url}")
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
            
    logger.info(f"Download complete: {target_path}")


def fetch_taxi_data(year, month, color='yellow'):
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-{month:02d}.parquet"
    target_path = f"data/raw/{color}/{year}-{month:02d}.parquet"
    download_file(url, target_path)
    return target_path


def fetch_zone_lookup():
    url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
    target_path = "data/raw/taxi_zone_lookup.csv"
    download_file(url, target_path)
    return target_path


def ingest_to_db(file_path, table_name, db_connector):
    logger.info(f"Ingesting parquet file: {file_path}")
    db_connector.execute(f"DROP TABLE IF EXISTS {table_name}")
    db_connector.execute(
        f"CREATE TABLE {table_name} AS SELECT * FROM read_parquet('{file_path}')"
    )
    row_count = db_connector.query_to_df(f"SELECT COUNT(*) as cnt FROM {table_name}")
    logger.info(f"Ingested {file_path} -> {table_name} ({row_count['cnt'].iloc[0]:,} rows)")


def ingest_csv_to_db(file_path, table_name, db_connector):
    logger.info(f"Ingesting CSV file: {file_path}")
    db_connector.execute(f"DROP TABLE IF EXISTS {table_name}")
    db_connector.execute(
        f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{file_path}')"
    )
    row_count = db_connector.query_to_df(f"SELECT COUNT(*) as cnt FROM {table_name}")
    logger.info(f"Ingested {file_path} -> {table_name} ({row_count['cnt'].iloc[0]:,} rows)")


if __name__ == "__main__":
    db = DBConnector()
    file_path = fetch_taxi_data(2024, 1)
    ingest_to_db(file_path, "raw_yellow_taxi", db)

    zone_path = fetch_zone_lookup()
    ingest_csv_to_db(zone_path, "taxi_zones", db)
    db.close()
