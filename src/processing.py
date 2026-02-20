import pandas as pd


def clean_data(df):
    df = df[df['trip_distance'] >= 0]
    df = df[df['fare_amount'] > 0]
    df = df.dropna(subset=['PULocationID', 'tpep_pickup_datetime'])
    return df


def extract_time_features(df):
    df = df.copy()
    df['pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['hour'] = df['pickup_datetime'].dt.hour
    df['day_of_week'] = df['pickup_datetime'].dt.dayofweek
    df['month'] = df['pickup_datetime'].dt.month
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    return df


def aggregate_demand(df):
    """Group rides by location + hour to get demand counts."""
    demand = (
        df.groupby(['PULocationID', 'hour', 'day_of_week', 'is_weekend'])
        .agg(
            ride_count=('VendorID', 'count'),
            avg_distance=('trip_distance', 'mean'),
            avg_fare=('fare_amount', 'mean'),
            avg_duration=('trip_distance', 'mean'),
        )
        .reset_index()
    )
    return demand
