from fastapi import FastAPI
import numpy as np

from src.inference.model import load_model
from src.inference.Features import build_features
from src.inference.confidence import assign_confidence_tier

app = FastAPI(title="LendSecure Realtime Price Prediction")

model = load_model()

@app.post("/predict")
def predict_price(payload: dict):
    """Predict property price given input data."""
    features = build_features(payload)
    pred_log = model.predict(features)
    predicted_price = float(np.expm1(pred_log))  # Inverse of log1p transformation

    result = {
        "predicted_price_usd": round(predicted_price,2),
        "confidence_tier": assign_confidence_tier({"predicted_price_usd": predicted_price})
    }


    return result
