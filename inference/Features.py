import pandas as pd
import numpy as mp
import json
from datetime import datetime
from pathlib import Path

ARTIFACT_DIR= Path("artifacts")
KNOWN_COUNTRIES_PATH = ARTIFACT_DIR / "known_countries.json"

with open(KNOWN_COUNTRIES_PATH, "r") as f:
    KNOWN_COUNTRIES = json.load(f)

CURRENT_YEAR = datetime.now().year


def build_features(input_data:dict) -> pd.DataFrame:
    """Build features for inference from input data."""
    df = df=pd.DataFrame([input_data])

    #country normailiztion
    df["country"]=(
        df["country"]
        .astype(str)
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    #one-hot encoding for known countries
    df=pd.get_dummies(df, columns=["country"])

    for country in KNOWN_COUNTRIES:
        country_col = f"country_{country}"
        if country_col not in df.columns:
            df[country_col] = 0

    #feature engineering
    df["building_age"] = CURRENT_YEAR - df["building_construction_year"]
    df.drop(columns=["building_construction_year"], inplace=True)

    df["log_apartment_total_area"] = mp.log1p(df["apartment_total_area"])
    df.drop(columns=["apartment_total_area"], inplace=True)

    df["location_freq"]=0.01
    df.drop(columns=["location"], inplace=True)

    feature_cols=[
        "apartment_rooms",
        "apartment_bathrooms",
        "building_total_floors",
        "building_age",
        "log_apartment_total_area",
        "location_freq",

    ]+ [f"country_{c}" for c in KNOWN_COUNTRIES]

    return df[feature_cols]
    
   