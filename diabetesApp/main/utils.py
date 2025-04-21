import json
import numpy as np
import pandas as pd
from joblib import load
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load model components
model = load(BASE_DIR / 'main/ml_models/diabetes_model.joblib')
scaler = load(BASE_DIR / 'main/ml_models/diabetes_scaler.joblib')
imputer = load(BASE_DIR / 'main/ml_models/diabetes_imputer.joblib')

# Load feature names
with open(BASE_DIR / 'main/ml_models/feature_names.json') as f:
    feature_names = json.load(f)

def validate_input(data):
    """Validate input data structure and values"""
    try:
        # Convert all values to float
        validated = {k: float(v) for k, v in data.items()}
        
        # Check we have all expected features
        if set(validated.keys()) != set(feature_names):
            missing = set(feature_names) - set(validated.keys())
            extra = set(validated.keys()) - set(feature_names)
            raise ValueError(f"Feature mismatch. Missing: {missing}, Extra: {extra}")
            
        return validated
    except ValueError as e:
        raise ValueError(f"Invalid input: {e}")

def preprocess_input(data):
    """Convert input data to properly shaped and scaled array"""
    # Convert to DataFrame to maintain feature names
    df = pd.DataFrame([data], columns=feature_names)
    
    # Impute missing values
    df_imputed = imputer.transform(df)
    
    # Scale features
    df_scaled = scaler.transform(df_imputed)
    
    return df_scaled, df_imputed