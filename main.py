from src.ingestion import fetch_taxi_data, ingest_to_db, fetch_zone_lookup, ingest_csv_to_db
from src.db import DBConnector

def run_ingestion():
    db = DBConnector()
    print("Starting data ingestion...")
    
    # Yellow Taxi Data
    file_path = fetch_taxi_data(2024, 1)
    ingest_to_db(file_path, "raw_yellow_taxi", db)
    
    # Zones
    zone_path = fetch_zone_lookup()
    ingest_csv_to_db(zone_path, "taxi_zones", db)
    
    print("Ingestion complete.")
    db.close()

if __name__ == "__main__":
    run_ingestion()
