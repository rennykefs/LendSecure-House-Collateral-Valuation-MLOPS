#-------------------
# Feature Engineering Script DAG 2
#-------------------
import pandas as pd
import numpy as np
from datetime import datetime
import mysql.connector
import json
from pathlib import Path
from datetime import datetime
import os
from dotenv import load_dotenv

#---------------------
# Database connection
#---------------------
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSOWRD"),
        database=os.getenv("DB_NAME")
    )

#--------------------------
# Loading cleaned data
#--------------------------
conn=get_connection()
df=pd.read_sql("SELECT * FROM data_cleaned",conn)
conn.close()

print("Loaded rows:",df.shape)

#--------------------------
# Target
#--------------------------
TARGET_COLUMN="price_in_USD"
current_year= datetime.now().year
df["country"]=(df["country"].astype(str).str.strip().str.replace(" ","_").str.replace("-","_"))


#--------------------------
# handle country/freeze schema
#------------------------
KNOWN_COUNTRIES=sorted(df["country"].dropna().unique().tolist())

#saving country list
artifact_dir=Path("artifacts")
artifact_dir.mkdir(exist_ok=True)

with open(artifact_dir / "known_countries.json","w") as f:
    json.dump(KNOWN_COUNTRIES,f)

print("Known countries saved:",KNOWN_COUNTRIES)



#--------------------------
# One-hot encode country
#--------------------------
df=pd.get_dummies(df,columns=["country"])

for country in KNOWN_COUNTRIES:
    col_name=f"country_{country}"
    if col_name not in df.columns:
        df[col_name]=0

#--------------------------
# Feature engineering
#--------------------------
#Building age
df["building_age"]=current_year - df["building_construction_year"]
df.drop(columns=["building_construction_year"],inplace=True)

#log area
df["log_apartment_total_area"]=np.log1p(df["apartment_total_area"])
df.drop(columns=["apartment_total_area"],inplace=True)

#Location frequency encoding
location_freq=df["location"].value_counts(normalize=True)
df["location_freq"]=df["location"].map(location_freq)
df.drop(columns=["location"],inplace=True)

# Median imputation
numeric_cols=[
    "apartment_rooms",
    "apartment_bathrooms",
    "building_total_floors",
    "building_age",
    "log_apartment_total_area",
    "location_freq"
]

for col in numeric_cols:
    df[col]=df[col].fillna(df[col].median())

#--------------------
# Final feature columns
#---------------------
country_cols=[f"country_{c}" for c in KNOWN_COUNTRIES]
final_columns=(["property_id"] + numeric_cols + country_cols + [TARGET_COLUMN])

df=df[final_columns]
print("Final feature shape:",df.shape)

#--------------------------
# Save features to feature store
#--------------------------
conn=get_connection()
cursor = conn.cursor()
insert_sql=f"""
INSERT INTO feature_engineered_properties (
    property_id,
    {",".join(numeric_cols)},
    {",".join(country_cols)},
    price_in_USD
    
)
VALUES (
    %s,
    {",".join(["%s"] * (len(numeric_cols) + len(country_cols) + 1))}
    
)
"""
for _,row in df.iterrows():
    cursor.execute(
        insert_sql,
        (
            row["property_id"],
            *[row[col] for col in numeric_cols],
            *[row[col] for col in country_cols],
            row[TARGET_COLUMN],
            

        )
       
       
        
    )
conn.commit()
cursor.close()
conn.close()

print("DAG 2 feature engineering completed successfully.")
print("Rows written:",len(df))
