def assign_confidence_tier(row):
    if row["predicted_price_usd"] <50000:
        return "Low Confidence"
    elif row["predicted_price_usd"] <200000:
        return "Medium Confidence"
    return "High Confidence"