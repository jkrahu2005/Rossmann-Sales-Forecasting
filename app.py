import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from datetime import date

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Rossmann Sales Dashboard",
    page_icon="📈",
    layout="wide"
)

# =====================================================
# CUSTOM STYLING
# =====================================================

st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}

[data-testid="metric-container"] {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.1);
}

h1 {
    color: #2563EB;
}

h2, h3 {
    color: #1e293b;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD MODEL & DATA
# =====================================================

model = joblib.load("models/xgb_model.pkl")
features = joblib.load("models/features.pkl")

# Load real dataset
df = pd.read_csv("data/train.csv")
df["Date"] = pd.to_datetime(df["Date"])

# =====================================================
# HEADER & SIDEBAR
# =====================================================

st.title("📊 Rossmann Store Sales Dashboard")
st.markdown("---")

# Sidebar branding
st.sidebar.title("📊 Rossmann BI Dashboard")
st.sidebar.markdown("Built using XGBoost + Streamlit")

page = st.sidebar.radio(
    "Navigation",
    [
        "Business Dashboard",
        "Sales Prediction",
        "What-If Simulator"
    ]
)

# =====================================================
# BUSINESS DASHBOARD
# =====================================================

if page == "Business Dashboard":

    st.header("📈 Business Insights")

    # KPI Section (4 metrics)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Model Accuracy (R²)", "97.67%")
    col2.metric("MAE", "332")
    col3.metric("RMSE", "474")
    col4.metric("Promo Lift", "+38.8%")

    st.markdown("---")

    # Executive Summary
    st.subheader("📌 Executive Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.info("📊 Records\n\n844,392")
    col2.success("🏆 Best Store Type\n\nB")
    col3.warning("🎄 Best Month\n\nDecember")
    col4.error("📈 Promo Impact\n\n+38.8%")

    st.markdown("---")

    # Monthly Sales Trend (from real data)
    st.subheader("📈 Monthly Sales Trend")
    df["Month"] = df["Date"].dt.month
    monthly_sales = df.groupby("Month")["Sales"].mean().reset_index()
    fig_line = px.line(
        monthly_sales,
        x="Month",
        y="Sales",
        markers=True,
        title="Average Sales by Month"
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # Promotion Impact (from real data)
    st.subheader("🎯 Promotion Impact")
    promo_df = df.groupby("Promo")["Sales"].mean().reset_index()
    promo_df["Promo"] = promo_df["Promo"].map({0: "No Promo", 1: "Promo"})
    fig_bar = px.bar(
        promo_df,
        x="Promo",
        y="Sales",
        title="Average Sales: Promo vs No Promo",
        text_auto=True
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # Feature Importance (from CSV)
    st.subheader("🚀 Top Business Drivers")
    feature_data = pd.read_csv("data/feature_importance.csv").head(10)
    fig_importance = px.bar(
        feature_data,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Top 10 Business Drivers",
        text_auto=".3f"
    )
    st.plotly_chart(fig_importance, use_container_width=True)

    st.markdown("---")

    # Key Business Findings
    st.subheader("📋 Key Business Findings")
    st.success("""
    ✅ Customers are the strongest sales driver.

    ✅ Promotional campaigns significantly boost sales.

    ✅ Store Type B and D outperform other store categories.

    ✅ December records highest average sales.

    ✅ Weekends generally observe lower sales.

    ✅ Competition distance has limited impact on revenue.

    ✅ Model explains 97.67% of sales variation.
    """)

# =====================================================
# SALES PREDICTION
# =====================================================

elif page == "Sales Prediction":

    st.header("🔮 Sales Prediction")
    st.write("Enter store information to estimate expected sales.")

    st.markdown("### Store Information")
    col1, col2 = st.columns(2)

    with col1:
        store = st.number_input("Store ID", min_value=1, value=1)
        customers = st.number_input("Expected Customers", min_value=0, value=500)
        competition_distance = st.number_input("Competition Distance (meters)", min_value=0.0, value=1000.0)

    with col2:
        selected_date = st.date_input("Date", value=date(2015, 12, 15))
        promo = st.selectbox("Promo Running?", ["No", "Yes"])
        promo2 = st.selectbox("Promo2 Active?", ["No", "Yes"])

    st.markdown("### Store Details")
    col3, col4 = st.columns(2)

    with col3:
        store_type = st.selectbox("Store Type", ["A", "B", "C", "D"])
        assortment = st.selectbox("Assortment", ["A", "B", "C"])

    with col4:
        school_holiday = st.selectbox("School Holiday", ["No", "Yes"])
        state_holiday = st.selectbox("State Holiday", ["0", "a", "b", "c"])

    st.markdown("")

    if st.button("Predict Sales", use_container_width=True):
        input_data = dict.fromkeys(features, 0)

        # Date features
        year = selected_date.year
        month = selected_date.month
        day = selected_date.day
        day_of_week = selected_date.weekday() + 1
        quarter = ((month - 1) // 3) + 1
        is_weekend = 1 if day_of_week >= 6 else 0

        # Basic features
        input_data["Store"] = store
        input_data["Customers"] = customers
        input_data["CompetitionDistance"] = competition_distance
        input_data["Promo"] = 1 if promo == "Yes" else 0
        input_data["Promo2"] = 1 if promo2 == "Yes" else 0
        input_data["SchoolHoliday"] = 1 if school_holiday == "Yes" else 0
        input_data["Open"] = 1
        input_data["Year"] = year
        input_data["Month"] = month
        input_data["Day"] = day
        input_data["DayOfWeek"] = day_of_week
        input_data["Quarter"] = quarter
        input_data["IsWeekend"] = is_weekend

        # Default values
        input_data["CompetitionOpenSinceMonth"] = 1
        input_data["CompetitionOpenSinceYear"] = 2010
        input_data["Promo2SinceWeek"] = 1
        input_data["Promo2SinceYear"] = 2012
        input_data["CompetitionAge"] = (year - 2010) * 12 + month
        input_data["PromoAge"] = (year - 2012) * 12 + month

        # Store type
        if store_type == "B":
            input_data["StoreType_b"] = 1
        elif store_type == "C":
            input_data["StoreType_c"] = 1
        elif store_type == "D":
            input_data["StoreType_d"] = 1

        # Assortment
        if assortment == "B":
            input_data["Assortment_b"] = 1
        elif assortment == "C":
            input_data["Assortment_c"] = 1

        # State holiday
        if state_holiday == "0":
            input_data["StateHoliday_0"] = 1
        elif state_holiday == "a":
            input_data["StateHoliday_a"] = 1
        elif state_holiday == "b":
            input_data["StateHoliday_b"] = 1
        elif state_holiday == "c":
            input_data["StateHoliday_c"] = 1

        # Promo interval
        if promo2 == "Yes":
            input_data["PromoInterval_Jan,Apr,Jul,Oct"] = 1
        else:
            input_data["PromoInterval_None"] = 1

        input_df = pd.DataFrame([input_data])
        prediction = model.predict(input_df)[0]

        st.balloons()
        st.success(f"Predicted Sales: ₹ {prediction:,.0f}")

        col1, col2 = st.columns(2)
        col1.metric("Expected Revenue", f"₹ {prediction:,.0f}")
        col2.metric("Store Traffic", customers)

        if promo == "Yes":
            st.info("Promotion is expected to positively impact sales.")
        else:
            st.warning("No promotion is currently active.")

# =====================================================
# WHAT-IF SIMULATOR (REAL PREDICTIONS)
# =====================================================

elif page == "What-If Simulator":

    st.header("🧪 Promotion Impact Simulator")
    st.write("Adjust the number of customers to see the estimated sales lift from running a promotion.")

    customers = st.slider("Expected Customers", min_value=100, max_value=3000, value=500, step=50)
    store_type = st.selectbox("Store Type", ["A", "B", "C", "D"])

    # Base input dictionary (default values)
    input_base = dict.fromkeys(features, 0)

    input_base["Store"] = 1
    input_base["Customers"] = customers
    input_base["Open"] = 1
    input_base["CompetitionDistance"] = 1000

    input_base["Year"] = 2015
    input_base["Month"] = 12
    input_base["Day"] = 15
    input_base["DayOfWeek"] = 2
    input_base["Quarter"] = 4

    input_base["CompetitionOpenSinceMonth"] = 1
    input_base["CompetitionOpenSinceYear"] = 2010
    input_base["Promo2SinceWeek"] = 1
    input_base["Promo2SinceYear"] = 2012

    input_base["CompetitionAge"] = 72
    input_base["PromoAge"] = 36

    # Store type encoding
    if store_type == "B":
        input_base["StoreType_b"] = 1
    elif store_type == "C":
        input_base["StoreType_c"] = 1
    elif store_type == "D":
        input_base["StoreType_d"] = 1

    # Two scenarios
    no_promo = input_base.copy()
    with_promo = input_base.copy()
    no_promo["Promo"] = 0
    with_promo["Promo"] = 1

    no_promo_pred = model.predict(pd.DataFrame([no_promo]))[0]
    with_promo_pred = model.predict(pd.DataFrame([with_promo]))[0]

    uplift = ((with_promo_pred - no_promo_pred) / no_promo_pred) * 100

    col1, col2 = st.columns(2)
    col1.metric("Without Promo", f"₹ {no_promo_pred:,.0f}")
    col2.metric("With Promo", f"₹ {with_promo_pred:,.0f}")

    st.success(f"Estimated Sales Lift: {uplift:.1f}%")

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")
st.caption("Built by Rahul Kumar | Rossmann Sales Forecasting & Business Intelligence Dashboard")