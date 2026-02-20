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


def run_training():
    from src.model import train_baseline, train_xgboost, evaluate, save_model
    from src.dataset import prepare_datasets

    db = DBConnector()
    df = db.query_to_df("SELECT * FROM demand_features")
    db.close()

    X_train, X_test, y_train, y_test = prepare_datasets(df)

    print("\n=== Training ===")
    lr = train_baseline(X_train, y_train)
    lr_m = evaluate(lr, X_test, y_test)
    save_model(lr, lr_m, "linear_regression")

    xgb = train_xgboost(X_train, y_train)
    xgb_m = evaluate(xgb, X_test, y_test)
    save_model(xgb, xgb_m, "xgboost")


def run_predict(location_id, hour, day_of_week):
    from src.inference import get_latest_model, load_model, predict_demand
    model = load_model(get_latest_model())
    result = predict_demand(model, location_id, hour, day_of_week)
    print(f"Predicted demand: {result} rides")


def main():
    parser = argparse.ArgumentParser(description="NYC Taxi Demand Pipeline")
    parser.add_argument('--step', choices=['ingest', 'etl', 'train', 'predict', 'all'],
                        default='all')
    parser.add_argument('--location', type=int, default=161)
    parser.add_argument('--hour', type=int, default=17)
    parser.add_argument('--dow', type=int, default=2, help="day of week (0=Mon)")
    args = parser.parse_args()

    if args.step in ('ingest', 'all'):
        run_ingestion()
    if args.step in ('etl', 'all'):
        run_etl()
    if args.step in ('train', 'all'):
        run_training()
    if args.step == 'predict':
        run_predict(args.location, args.hour, args.dow)


if __name__ == "__main__":
    main()
