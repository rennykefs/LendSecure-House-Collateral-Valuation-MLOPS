#--------------
# Imports
#--------------
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

import mlflow
import mlflow.sklearn
import mysql.connector
import os
from dotenv import load_dotenv


#-------------
#Mysql connection
#-------------
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSOWRD"),
        database=os.getenv("DB_NAME")

    )

#--------------
# MLflow setup
#--------------

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("LENDSECURE_MODEL_EXPERIMENT")
print("Tracking URI:", mlflow.get_tracking_uri())



#--------------
# Load Data
#--------------
conn=get_connection()
query="SELECT * FROM feature_engineered_properties"
df= pd.read_sql(query,conn)
conn.close()
print ("Training rows:", df.shape)

#--------------
# Data Preparation
#--------------
TARGET_COLUMN="price_in_USD"
BASE_NUMERIC_FEATURES=[
    "apartment_rooms",
    "apartment_bathrooms",
    "building_total_floors",
    "building_age",
    "log_apartment_total_area",
    "location_freq"
]
COUNTRY_FEATURES=[col for col in df.columns if col.startswith( "country_")]
FEATURE_COLUMNS=BASE_NUMERIC_FEATURES + COUNTRY_FEATURES
X=df[FEATURE_COLUMNS]
y=df[TARGET_COLUMN]  

non_numeric_cols=X.select_dtypes(exclude=["number"]).columns
if len(non_numeric_cols)>0:
    raise ValueError(f"Non-numeric columns found in X: {non_numeric_cols}")




X_train,X_val,y_train,y_val=train_test_split(X,y,test_size=0.2,random_state=42)

#--------------
# Model Training and Evaluation
#--------------
with mlflow.start_run(run_name="randomforest_LendSecure"):
    model=RandomForestRegressor(n_estimators=50,max_depth=20,random_state=42,n_jobs=-1)

    model.fit(X_train,y_train)

    # Validation
    preds=model.predict(X_val)

    mae=mean_absolute_error(y_val,preds)
    rmse=root_mean_squared_error(y_val,preds)
    r2=r2_score(y_val,preds)

    

    # Log parameters and metrics
    mlflow.log_metric("mae",mae)
    mlflow.log_metric("rsme",rmse)
    mlflow.log_metric("r2",r2)
    mlflow.log_param("model_type","RandomForestRegressor")
    mlflow.log_param("n_estimators",300)


    

    

    # Log the model
    mlflow.sklearn.log_model(sk_model=model,artifact_path="model",registered_model_name="LendSecure_Price_Prediction_Model")

    run_id = mlflow.active_run().info.run_id

print("DAG 3 completed")
print("RMSE:", rmse)
print("MAE:" , mae)
print("R2:", r2)
