import os
import json
import joblib
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

from src.db import DBConnector
from src.dataset import prepare_datasets


MODELS_DIR = "models"


def train_baseline(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def evaluate(model, X_test, y_test):
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    return {"mae": round(mae, 4), "rmse": round(rmse, 4)}


def save_model(model, metrics, name="baseline"):
    os.makedirs(MODELS_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = os.path.join(MODELS_DIR, f"{name}_{ts}.joblib")
    joblib.dump(model, model_path)

    metrics_path = os.path.join(MODELS_DIR, f"{name}_{ts}_metrics.json")
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)

    print(f"Model saved: {model_path}")
    print(f"Metrics: {metrics}")
    return model_path


if __name__ == "__main__":
    db = DBConnector()
    df = db.query_to_df("SELECT * FROM demand_features")
    db.close()

    X_train, X_test, y_train, y_test = prepare_datasets(df)
    model = train_baseline(X_train, y_train)
    metrics = evaluate(model, X_test, y_test)
    save_model(model, metrics, "linear_regression")
