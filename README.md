# 🛒 Product Sales Forecasting & Prediction App

This Flask web application lets you:
- Upload a CSV to predict **daily sales** using a trained XGBoost model
- Enter data manually for single-point prediction
- Generate **weekly sales forecasts** using a Prophet time series model
- View results in an **interactive table**
- Run locally or as a **Docker container**

---

## 📁 Project Structure

project-root/
├── app.py
├── models/
│ ├── xgb_model.pkl
│ └── prophet_model.pkl
├── templates/
│ └── index.html
├── static/
├── requirements.txt
├── Dockerfile
└── README.md


---

## 🚀 Run Locally

```bash
# Clone repo and move into it
git clone https://github.com/your-username/product-sales-app.git
cd product-sales-app

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows use venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py


# DOCKER PART
# Build image
docker build -t product-sales-app .

# Run container
docker run -p 5000:5000 product-sales-app


Then open: http://localhost:5000



📝 Features
    📁 CSV Upload
    📈 Prophet Forecast for next 12 weeks
    📊 Interactive prediction table
    🧠 XGBoost for predictions
    ⏱️ Prophet for time series forecasting
    🐳 Docker compatible
    ✅ Deployment Ready


Forecasting Route

Hit the /forecast route via browser to get Prophet-based forecast for the next 12 weeks.

🧪 Model Details

XGBoost MAE: ₹2435.30

Prophet trained on weekly sales data (2018–2019)

SARIMA and ARIMA were evaluated, but Prophet selected as best forecaster

📊 Tableau Dashboard

Tableau dashboards available https://public.tableau.com/shared/S798Z4NRG?:display_count=n&:origin=viz_share_link
 
Technical blog : https://medium.com/@koshi.gg23/forecasting-the-future-a-full-stack-approach-to-product-sales-forecasting-in-retail-8e9c1930dfe7


Push this repo to GitHub and deploy using services like:

    Heroku
    Railway
    Render
    EC2
    or your own on-prem server

🧑‍💻 Author

Name: Kousalya R

Date: August 2025

Version: 1.0

Last Updated: 2025-08-21 18:47:33