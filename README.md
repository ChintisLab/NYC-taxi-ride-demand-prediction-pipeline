# NYC Taxi Ride Demand Prediction Pipeline

Local implementation of an end-to-end data pipeline for NYC taxi demand forecasting.

## Architecture

```
Raw Data (Parquet) → Ingestion → DuckDB → ETL → Feature Store → ML Models → Predictions
```

- **Data Storage**: DuckDB (local analytical database)
- **ETL**: Python + Pandas
- **ML Models**: Linear Regression, XGBoost
- **Visualization**: Streamlit (coming soon)

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run the full pipeline (ingest, ETL, train):
```bash
python main.py --step all
```

**Launch the Dashboard** (Interactive Web App):
```bash
python main.py --step dashboard
```

Run individual steps:
```bash
python main.py --step ingest    # download and load raw data
python main.py --step etl       # clean, transform, aggregate
python main.py --step train     # train LR + XGBoost models
python main.py --step predict --location 161 --hour 17 --dow 2
```

## Project Structure

```
├── main.py                 # CLI orchestrator
├── src/
│   ├── db.py               # DuckDB connection wrapper
│   ├── ingestion.py         # data download + DB loading
│   ├── processing.py        # cleaning + feature engineering
│   ├── etl_pipeline.py      # end-to-end ETL job
│   ├── dataset.py           # train/test splitting
│   ├── model.py             # model training + evaluation
│   ├── inference.py         # load model + predict demand
│   └── visualization.py     # streamlit dashboard (WIP)
├── data/                    # local data lake (gitignored)
├── models/                  # saved model artifacts (gitignored)
└── requirements.txt
```

## Data Source
NYC TLC Trip Record Data: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
