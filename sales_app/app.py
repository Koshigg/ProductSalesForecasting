import os
import pickle
import pandas as pd
from flask import Flask, request, render_template
from xgboost import XGBRegressor
from prophet import Prophet

app = Flask(__name__)

# Load saved models
xgb_model = pickle.load(open("models/xgb_model.pkl", "rb"))
prophet_model = pickle.load(open("models/prophet_model.pkl", "rb"))

# Define expected feature columns for prediction
FEATURE_COLS = [
    'Store_id', 'Holiday', 'Orders', 'Year', 'Month', 'Week', 'Day', 'DayOfWeek', 'Is_Weekend',
    'Store_Type_S2', 'Store_Type_S3', 'Store_Type_S4',
    'Location_Type_L2', 'Location_Type_L3', 'Location_Type_L4', 'Location_Type_L5',
    'Region_Code_R2', 'Region_Code_R3', 'Region_Code_R4',
    'Discount_Yes'
]

# Helper function to preprocess inputs
def preprocess(df):
    # One-hot encode required categorical columns
    cat_cols = ['Store_Type', 'Location_Type', 'Region_Code', 'Discount']
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

    # Align columns to match training structure
    df, _ = df.align(pd.DataFrame(columns=FEATURE_COLS), join='right', axis=1, fill_value=0)
    return df

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict_csv", methods=["POST"])
def predict_csv():
    file = request.files["file"]
    if not file:
        return "No file uploaded", 400

    df = pd.read_csv(file)
    df_processed = preprocess(df.copy())
    predictions = xgb_model.predict(df_processed)
    df["Predicted_Sales"] = predictions.round(2)

    return render_template("index.html", predictions=df)

@app.route("/predict_manual", methods=["POST"])
def predict_manual():
    input_dict = {key: request.form[key] for key in request.form}
    df = pd.DataFrame([input_dict])

    # Cast correct data types
    numeric_cols = ['Store_id', 'Holiday', 'Orders', 'Year', 'Month', 'Week', 'Day', 'DayOfWeek', 'Is_Weekend']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col])

    df_processed = preprocess(df.copy())
    prediction = xgb_model.predict(df_processed)[0]

    df["Predicted_Sales"] = round(prediction, 2)
    return render_template("index.html", predictions=df)

@app.route("/forecast", methods=["GET"])
def forecast():
    future = prophet_model.make_future_dataframe(periods=12, freq='W')  # 12 weeks
    forecast_df = prophet_model.predict(future)
    result = forecast_df[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(12)
    result.rename(columns={"ds": "Date", "yhat": "Forecast", "yhat_lower": "Lower Bound", "yhat_upper": "Upper Bound"}, inplace=True)

    return render_template("index.html", predictions=result)

if __name__ == "__main__":
    app.run(debug=True)
