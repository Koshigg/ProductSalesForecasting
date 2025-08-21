import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
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

def plot_forecast(forecast_df):
    plt.figure(figsize=(10, 6))
    plt.plot(forecast_df["Date"], forecast_df["Forecast"], label="Forecast", color='blue')
    plt.fill_between(
        forecast_df["Date"],
        forecast_df["Lower Bound"],
        forecast_df["Upper Bound"],
        color="skyblue",
        alpha=0.3,
        label="Confidence Interval"
    )
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Sales Forecast")
    plt.title("📈 Prophet Sales Forecast (Next 12 Weeks)")
    plt.legend()
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url

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

    # Generate forecast using Prophet
    future = prophet_model.make_future_dataframe(periods=12, freq='W')
    forecast_df = prophet_model.predict(future)
    result = forecast_df[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(12)
    result.rename(columns={"ds": "Date", "yhat": "Forecast", "yhat_lower": "Lower Bound", "yhat_upper": "Upper Bound"}, inplace=True)

    # Save forecast for chart rendering
    forecast_data = result.to_dict(orient="records")

    return render_template("index.html", predictions=df, forecast_data=forecast_data)


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
    future = prophet_model.make_future_dataframe(periods=12, freq='W')
    forecast_df = prophet_model.predict(future)

    result = forecast_df[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(12)
    result.rename(columns={"ds": "Date", "yhat": "Forecast", "yhat_lower": "Lower Bound", "yhat_upper": "Upper Bound"}, inplace=True)

    chart = plot_forecast(result)

    return render_template("index.html", predictions=result, forecast_chart=chart)



if __name__ == "__main__":
    app.run(debug=True)
