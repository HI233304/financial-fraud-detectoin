import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from pathlib import Path

def load_data(path=None):
    if path:
        df = pd.read_csv(path)
    else:
        here = Path(__file__).resolve().parent.parent
        df = pd.read_csv(here / "data" / "sample_transactions.csv")
    return df

def build_preprocessor(df: pd.DataFrame):
    # numeric and categorical columns
    num_cols = ["amount","time_delta","typing_speed_ms","device_trust","is_night"]
    cat_cols = ["merchant_cat","country"]
    pre = ColumnTransformer([
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
    ])
    return pre, num_cols, cat_cols

def prepare_xy(df: pd.DataFrame):
    y = df["is_fraud"].astype(int)
    X = df.drop(columns=["is_fraud"])
    return X, y

def train_test_split(df, test_size=0.2, random_state=42):
    X, y = prepare_xy(df)
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
