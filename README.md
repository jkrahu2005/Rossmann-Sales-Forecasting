# 📊 Rossmann Retail Sales Forecasting & Business Intelligence Dashboard

## Overview

This project is an end-to-end Retail Sales Forecasting and Business Intelligence platform built using the Rossmann Store Sales dataset.

The solution combines data analysis, machine learning, and interactive business dashboards to help predict future store sales and generate actionable business insights.

---

## Problem Statement

Retail businesses need accurate sales forecasts to optimize:

* Inventory planning
* Promotion strategies
* Workforce management
* Revenue forecasting

This project predicts daily store sales using historical sales, promotions, store information, competition data, and seasonal trends.

---

## Dataset

Dataset Source:

* Rossmann Store Sales (Kaggle)

Records:

* 844,392+

Features:

* 31 engineered features

---

## Tech Stack

### Data Analysis

* Pandas
* NumPy

### Visualization

* Plotly
* Matplotlib
* Seaborn

### Machine Learning

* XGBoost

### Deployment

* Streamlit

---

## Key Features

### Business Dashboard

* Executive KPI Summary
* Monthly Sales Trends
* Promotion Impact Analysis
* Feature Importance Analysis

### Sales Prediction

* Interactive forecasting tool
* Business-friendly inputs
* Real-time prediction

### What-If Simulator

* Promotion impact estimation
* Revenue uplift analysis

---

## Model Performance

| Metric   |  Value |
| -------- | -----: |
| R² Score | 0.9767 |
| MAE      | 331.98 |
| RMSE     | 474.45 |

---

## Key Business Insights

* Customers are the strongest driver of sales.
* Promotions significantly improve revenue.
* Store Type B consistently outperforms other store types.
* December shows the highest average sales.
* Competition distance has limited impact on revenue.

---

## Project Structure

Rossmann-Sales-Forecasting/

├── app.py
├── requirements.txt
├── README.md

├── data/
├── models/
├── notebooks/
├── reports/
├── screenshots/

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
