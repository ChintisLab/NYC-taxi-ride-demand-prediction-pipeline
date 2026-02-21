import pandas as pd


def split_features_target(df, target_col='ride_count'):
    feature_cols = ['PULocationID', 'hour', 'day_of_week', 'is_weekend']
    X = df[feature_cols]
    y = df[target_col]
    return X, y


def temporal_split(df, test_ratio=0.2):
    """Split keeping the last N% of data as test (simulates time-based split)."""
    split_idx = int(len(df) * (1 - test_ratio))
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]
    return train_df, test_df


def prepare_datasets(df):
    train_df, test_df = temporal_split(df)
    X_train, y_train = split_features_target(train_df)
    X_test, y_test = split_features_target(test_df)
    print(f"Train: {len(X_train)} samples, Test: {len(X_test)} samples")
    return X_train, X_test, y_train, y_test
