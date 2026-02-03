print("Running file:", __file__)


#---------------------------
# libaries importations
#---------------------------
import pandas as pd
import numpy as np
from datetime import datetime
import mysql.connector
import os
from dotenv import load_dotenv


#--------------
# Database connection
#--------------
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSOWRD"),
        database=os.getenv("DB_NAME")
    )
   
#--------------------------
# Loading data
#--------------------------
CSV_PATH = r"C:\Users\Jones Mbela\Desktop\RENNY\AI AND ML\Lend Secure\Data\world_real_estate_data(147k).csv"
df= pd.read_csv(CSV_PATH)

print("Initial shape:",df.shape)

#--------------------------
# Drop Columns
#--------------------------
drop_columns=[
    "url",
    "image",
    "title",
    "apartment_bedrooms",
    "apartment_floor",
    "apartment_living_area",
]
df=df.drop(columns=[c for c in drop_columns if c in df.columns])

#--------------------------
# Target cleaning
#--------------------------
target_column="price_in_USD"
df=df[df[target_column]>0]

#--------------------------
# Fixing data types
#--------------------------
if "apartment_total_area" in df.columns:
    df["apartment_total_area"]=(
        df["apartment_total_area"]
        .astype(str)
        .str.replace(r"[^\d.]","",regex=True)
        .replace("",np.nan)
        .astype(float)
    )

#--------------------------
# sanity Cleaning
#--------------------------
current_year=datetime.now().year
if "building_construction_year" in df.columns:
    df.loc[
        (df["building_construction_year"]<1800) | 
        (df["building_construction_year"]>current_year),
        "building_construction_year"
    ]=np.nan
numric_columns=[
    "apartment_rooms",
    "apartment_bathrooms",
    "building_total_floors"
    
]
for col in numric_columns:
    if col in df.columns:
        df.loc[df[col]<0,col]=np.nan
        df[col]=df[col].fillna(df[col].median())

#--------------------------
# Categorical handling
#--------------------------
df["country"]=df["country"].fillna(df["country"].mode()[0])
df["location"]=df["location"].fillna("Unknown")
df= df.replace({np.nan:None})

#--------------------------
# insert cleaned data into database
#--------------------------
conn=get_connection()
cursor=conn.cursor()
insert_sql="""
INSERT INTO data_cleaned(

    apartment_total_area,
    apartment_rooms,
    apartment_bathrooms,
    building_total_floors,
    building_construction_year,
    country,
    location,
    price_in_USD
) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
"""
for _,row in df.iterrows():
    cursor.execute(insert_sql,(
    
        row['apartment_total_area'],
        row['apartment_rooms'],
        row['apartment_bathrooms'],
        row['building_total_floors'],
        row['building_construction_year'],
        row['country'],
        row['location'],
        row['price_in_USD'],
                
       
    ))
conn.commit()
cursor.close()
conn.close()
print("DAG 1 ingestion completed successfully.")

