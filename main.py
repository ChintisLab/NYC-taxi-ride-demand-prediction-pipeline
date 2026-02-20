import argparse
from src.ingestion import fetch_taxi_data, ingest_to_db, fetch_zone_lookup, ingest_csv_to_db
from src.etl_pipeline import run_etl
from src.db import DBConnector


def run_ingestion():
    db = DBConnector()
    print("=== Data Ingestion ===")

    file_path = fetch_taxi_data(2024, 1)
    ingest_to_db(file_path, "raw_yellow_taxi", db)

    zone_path = fetch_zone_lookup()
    ingest_csv_to_db(zone_path, "taxi_zones", db)

    print("Ingestion complete.\n")
    db.close()


def main():
    parser = argparse.ArgumentParser(description="NYC Taxi Demand Pipeline")
    parser.add_argument('--step', choices=['ingest', 'etl', 'all'], default='all')
    args = parser.parse_args()

    if args.step in ('ingest', 'all'):
        run_ingestion()
    if args.step in ('etl', 'all'):
        run_etl()


if __name__ == "__main__":
    main()
