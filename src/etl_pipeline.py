from src.db import DBConnector
from src.processing import clean_data, extract_time_features, aggregate_demand
from src.logger import get_logger

logger = get_logger(__name__)

def run_etl():
    db = DBConnector()

    logger.info("Running ETL pipeline...")
    raw_df = db.query_to_df("SELECT * FROM raw_yellow_taxi")
    logger.info(f"Loaded {len(raw_df):,} raw rows from database")

    cleaned = clean_data(raw_df)
    logger.info(f"After cleaning: {len(cleaned):,} rows remaining")

    featured = extract_time_features(cleaned)

    demand = aggregate_demand(featured)
    logger.info(f"Aggregated into {len(demand):,} demand records")

    db.execute("DROP TABLE IF EXISTS demand_features")
    db.conn.execute("CREATE TABLE demand_features AS SELECT * FROM demand", {"demand": demand})
    logger.info("Stored demand_features table successfully in DuckDB")

    db.close()
    return demand


if __name__ == "__main__":
    run_etl()
