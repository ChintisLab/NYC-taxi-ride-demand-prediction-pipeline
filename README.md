# NYC Taxi Ride Demand Prediction Pipeline

A complete, end-to-end local data pipeline for NYC taxi demand forecasting. This project ingests raw parquets, runs an ETL process into a local DuckDB data warehouse, trains machine learning models (XGBoost), and serves predictions via an interactive Streamlit dashboard.

## Architecture

```
Raw Data (Parquet/CSV) → Ingestion → DuckDB → ETL → Feature Store → ML Models → Streamlit Dashboard
```

- **Data Storage**: DuckDB (local analytical database)
- **ETL**: Python + Pandas
- **ML Models**: scikit-learn (Linear Regression), XGBoost
- **Visualization**: Streamlit

## Local Setup

These steps will get the pipeline running on your local machine from scratch:

1. **Clone the repository and set up a virtual environment:**
```bash
git clone https://github.com/ChintisLab/NYC-taxi-ride-demand-prediction-pipeline.git
cd NYC-taxi-ride-demand-prediction-pipeline
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the pipeline (downloads data, builds DB, trains models):**
```bash
python main.py --step all
```

4. **Launch the interactive dashboard:**
```bash
python main.py --step dashboard
```
The dashboard will open automatically in your browser at `http://localhost:8501`.

## CLI Usage Options

You can run individual steps of the pipeline if you're developing specific components:
```bash
python main.py --step ingest    # downloads and loads raw data to DuckDB
python main.py --step etl       # cleans data, engineers features, and aggregates demand
python main.py --step train     # trains Linear Regression + XGBoost models
python main.py --step predict --location 161 --hour 17 --dow 2 # quickly test inference directly in CLI
```


## Project Structure

```
├── main.py                 # CLI orchestrator
├── src/
│   ├── db.py               # DuckDB connection wrapper
│   ├── ingestion.py        # data download + DB loading
│   ├── processing.py       # cleaning + feature engineering
│   ├── etl_pipeline.py     # end-to-end local ETL job
│   ├── dataset.py          # train/test splitting routines
│   ├── model.py            # model training + evaluation
│   ├── inference.py        # load model + predict utility
│   ├── logger.py           # standardized console logger
│   └── visualization.py    # streamlining web dashboard
├── data/                   # local data lake & duckdb file (gitignored by default)
├── models/                 # saved model joblib artifacts (gitignored by default)
└── requirements.txt        # python dependencies
```

## Data Source
NYC TLC Trip Record Data: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
