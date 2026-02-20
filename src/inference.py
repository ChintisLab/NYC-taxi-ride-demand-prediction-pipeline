import os
import glob
import joblib
import pandas as pd


def get_latest_model(model_dir="models", prefix="xgboost"):
    pattern = os.path.join(model_dir, f"{prefix}_*.joblib")
    files = sorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No model found with prefix '{prefix}' in {model_dir}")
    return files[-1]


def load_model(model_path):
    return joblib.load(model_path)


def predict_demand(model, location_id, hour, day_of_week):
    is_weekend = 1 if day_of_week in [5, 6] else 0
    features = pd.DataFrame([{
        "PULocationID": location_id,
        "hour": hour,
        "day_of_week": day_of_week,
        "is_weekend": is_weekend,
    }])
    prediction = model.predict(features)[0]
    return max(0, round(prediction, 2))


if __name__ == "__main__":
    model_path = get_latest_model()
    model = load_model(model_path)
    print(f"Loaded model: {model_path}")

    result = predict_demand(model, location_id=161, hour=17, day_of_week=2)
    print(f"Predicted demand for LocationID=161, 5PM Tuesday: {result} rides")
