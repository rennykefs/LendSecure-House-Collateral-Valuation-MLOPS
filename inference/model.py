import mlflow

MODEL_NAME="LendSecure_Price_Prediction_Model"
MODEL_ALIAS="Production"

mlflow.set_tracking_uri("http://127.0.0.1:5000")

def load_model():
    model_uri = f"models:/{MODEL_NAME}@{MODEL_ALIAS}"
    return mlflow.pyfunc.load_model(model_uri)