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

## Deployment (Streamlit Community Cloud)

You can easily deploy this dashboard to the public web for free using [Streamlit Community Cloud](https://streamlit.io/cloud).

### Prerequisites
Before deploying, make sure your GitHub repository is public (or you have a Streamlit account connected to your private repo) and that you have run the pipeline locally at least once so the `models/` directory has a trained `.joblib` model.

1. **Commit your trained models and data (Optional but recommended for Cloud):**
By default, the `data/` and `models/` directories are gitignored. Since Streamlit Cloud doesn't run the `main.py` ingestion/training steps automatically on boot, you need to provide the pre-trained database and models. 
   - Remove `data/` and `models/` from your `.gitignore`.
   - Commit and push your local `data/taxi_data.db` and the `.joblib` model files to GitHub.

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
   - Click **"New app"**.
   - Select your repository (`ChintisLab/NYC-taxi-ride-demand-prediction-pipeline`).
   - Set the Main file path to: `src/visualization.py`
   - Click **"Deploy!"**

Your app will take a minute or two to bake and install the `requirements.txt`. Once finished, Streamlit will give you a public URL you can share!

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
