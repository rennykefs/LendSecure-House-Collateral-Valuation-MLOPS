# LendSecure-House-Collateral-Valuation System
End-to-end MLOps Pipeline for Real Estate Collateral Valuation

## 1. Project Overview
Lendsecure is a machine learning system designed to estimate the market value of real estate properties for use as loan collateral.
The project implements a full production-grade workflow from data ingestion to real time inference using modern MLOps principles.

The system enables financial institutions to:
- Automate property evaluation
- Reduce manual appraisal time.
- Standardize Collateral assessment
- Support faster loan approvals

## 2. Features
- Automated data ingestion from CSV to MySQL
- Data cleaning and validation Pipeline
- Feature Engineering Workflow
- Model training with Mlflow tracking
- Model Registry and Versioning
- Real-Time Inference API
- Confidence Tier Scoring
- Production-Ready Modular Codebase

## 3. Architecture
The system follows a modular DAG-based architecture:
### 3.1 DAG 1- Data Ingestion
- Raw property data uploaded as CSV
- Exploratory Data Analysis (EDA) performed
- Data cleaning pipeline executed
- Cleaned data stored in MySQL database

### 3.2 DAG 2-Feature Engineering
- Data retrieved from MySQL
- Transformations applied
- One-hot encoding with schema freezing
- Features stored for model training

### 3.3 DAG 3- Model Training
- Feature data loaded
- Model trained using Random Forest
- Hyperparemeter tuning
- Metrics logged to MLflow
- Best model registered to Mlflow Model Registry

### 3.4 DAG 4- Real Time inference
- FAST API for on demand predictions
- Confidence tier Assignments
- Instant valuation results

## 4. Tech Stack
| Component | Technology |
|-----------|------------|
Language | Python |
Database | MySQL |
ML Tracking | MLflow |
Model type | Random Forest Regressor |
API Framework | Fast API |
Environment | Virtualenv |
Version Control | Git/Github |

## 5. Model Details
- Algorithm: Random Forest Regressor
- Evaluation Metrics: RMSE, MAE,R2 Score
  
 Mlflow is used to:
- Track experiments
- Compare model versions
- Register best-performing models
- Enable reproducability

## 6. Future Improvements
- Intergration with Feast feature Store
- Automated retraining pipeline
- Model monitoring and drift detection
- Dashboard with streamlit
- CI/CD pipeline intergration

## Contributions are welcome! feel free to submit pull requests or raises issues

## Author
Reinhardt Kefa
-Data Scientist | ML Engineer
- Passionate about MLOps and AI-driven systems 






