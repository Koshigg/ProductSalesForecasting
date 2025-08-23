# 🔮 Forecasting the Future: A Full-Stack Approach to Product Sales Forecasting in Retail

**By Kousalya R**

---

In today’s competitive retail landscape, the ability to anticipate demand can be the difference between a thriving business and one that struggles with excess inventory or lost sales opportunities. That’s why I took on a real-world data science challenge — building a product sales forecasting system that not only delivers predictions but also makes them actionable through dashboards and APIs.

In this post, I’ll walk you through my end-to-end pipeline:

- 📊 Tableau dashboards for business insights  
- 🔍 EDA and hypothesis testing to understand sales drivers  
- 🤖 Machine learning and time series modeling  
- 🚀 Flask API deployment for real-time usage  

Let’s dive in.

---

## 🧩 Problem Statement: Why Forecast Sales?

Retailers deal with questions like:

- How much inventory should we stock next week?
- Will upcoming holidays impact our sales?
- Are discounts actually increasing our revenue?

To answer these, I built a sales forecasting solution using historical store-level data enriched with attributes like store type, region, discounts, holidays, and more.

---

## 📦 Dataset at a Glance

The dataset (publicly available [here](https://drive.google.com/drive/folders/1fBQ1PlWMho3kHF9qXrD0McZNfpJIcbrn)) contains daily sales data for multiple stores, with features like:

- `Store_Type`, `Location_Type`, `Region_Code`
- `Date`, `Holiday`, `Discount`  
- `#Order`: Number of orders  
- `Sales`: Total daily sales (target)

---

## 📊 Tableau Dashboards: Insights Before Modeling

Before building any models, I turned to **Tableau** to understand what drives sales.

### 1. **Time Series Drill-Down**
A line chart with drill-down from year → quarter → month → day revealed seasonal trends and weekday effects.

### 2. **Sales by Store & Location**
Bar charts highlighted how store types and urban vs. rural locations differ in performance.

### 3. **Regional Analysis**
By plotting region-wise metrics — total sales, order count, and average order size — I identified high-performing regions and underperformers.

### 4. **Promotions & Holidays**
I used box plots and bar charts to compare:
- Sales with vs. without discounts
- Sales on holidays vs. regular days

**Takeaway**: Discounts showed a strong positive effect on average sales, while some regions showed no significant holiday uplift — a potential insight for marketing teams.

### 5. **Operational Views**
A scatter plot between `#Order` and `Sales` helped spot anomalies — for instance, stores with high orders but low revenue (indicating small cart sizes).

> 💡 All dashboards included dynamic filters: store type, region, holiday, and date range — enabling slice-and-dice analysis.

---

## 🔍 EDA & Hypothesis Testing: Digging Deeper

### 📈 Exploratory Analysis
I performed univariate and bivariate analysis:
- Histograms for numerical variables like `Sales`, `#Order`
- Count plots for categorical variables
- Heatmaps for correlation

### 🧪 Hypothesis Testing Highlights

| Hypothesis | Test | Result |
|-----------|------|--------|
| Discounts increase sales | t-test | ✅ Confirmed |
| Holidays boost revenue | t-test | ✅ Confirmed |
| Store types impact sales | ANOVA | ✅ Confirmed |
| Regional sales vary | Kruskal-Wallis | ✅ Significant |
| More orders = more sales | Pearson correlation | ✅ Strong positive |

---

## 🤖 Modeling: From Linear Regression to Prophet

### 🧹 Data Preparation
- **Feature Engineering**: Lag variables, rolling averages, day-of-week encoding
- **Categorical Encoding**: One-hot and label encoding
- **Train-Test Split**: Time-based split to preserve temporal integrity

### 🧠 Models I Explored

#### 1. **Linear Regression**
Simple baseline using historical data + store features

#### 2. **XGBoost**
Tree-based regression model — handled nonlinear patterns, interaction effects

#### 3. **Prophet (Time Series)**
Facebook’s Prophet model automatically handles seasonality and holidays — ideal for univariate store-level forecasts

#### 4. **ARIMA/SARIMA**
Tried classical time series models to compare with Prophet

### 🧪 Evaluation Metrics
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- MAPE (Mean Absolute Percentage Error)

> 📉 Prophet and XGBoost gave the best trade-off between accuracy and interpretability.

---

## 🚀 Deployment: Flask App with Interactive Prediction

### 💡 Why Deploy?
Even the best model isn’t useful if it lives only in a notebook. I built a lightweight **Flask web app** to serve predictions and forecasts.

### 🔧 App Features
- **CSV Upload**: Get predictions for a batch of stores/days
- **Manual Entry**: Input features via form and get forecast
- **Forecast Route**: View next N days’ forecast from Prophet
- **Download Outlook .oft files**: For internal reporting use-case

### ⚙️ Tech Stack
- Flask for backend
- HTML + Bootstrap for frontend
- `pickle` to load the trained models
- Ready for Docker and cloud deployment (Azure/AWS)

---

## 📚 Key Learnings

- **EDA shapes modeling**: Patterns I saw in Tableau directly informed the features I engineered.
- **Model interpretability matters**: Tree-based models helped explain "why" a prediction was made.
- **Deployment completes the loop**: From data to decision, real-time predictions made the project useful.

---

## ✨ Wrapping Up

This project was more than just a modeling exercise — it was about building a data product. By combining analytics, machine learning, and deployment, I created a full-stack solution to solve a real retail problem.

> If you're a data scientist looking to go beyond notebooks — try building something end-to-end. That’s where the magic happens.

---


This Flask web application lets you:
- Upload a CSV to predict **daily sales** using a trained XGBoost model
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

Name: Kousalya R(Data Scientist)

Date: August 2025

Version: 1.0

Last Updated: 2025-08-21 18:47:33
