import pandas as pd

def clean_data(df):
    # Remove rows with negative trip distances
    df = df[df['trip_distance'] >= 0]
    
    # Remove rows with zero or negative fare amount
    df = df[df['fare_amount'] > 0]
    
    return df

def process_features(df):
    # Basic feature engineering: extraction of hour and day of week
    df['pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['hour'] = df['pickup_datetime'].dt.hour
    df['day_of_week'] = df['pickup_datetime'].dt.dayofweek
    
    return df
