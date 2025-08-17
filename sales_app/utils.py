# utils.py
import pandas as pd

def preprocess_input(df, model_columns):
    cat_cols = ['Store_Type', 'Location_Type', 'Region_Code', 'Discount']
    
    # One-hot encode categorical columns
    df_encoded = pd.get_dummies(df, columns=cat_cols, drop_first=True)
    
    # Align with training columns
    df_encoded, _ = df_encoded.align(model_columns, join='right', axis=1, fill_value=0)

    return df_encoded
