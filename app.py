import streamlit as st
import pandas as pd
import plotly.express as px

# Set page title
st.set_page_config(page_title="Digital Twin Business Simulator", layout="wide")

# Title and Description
st.title("🛩️ Digital Twin Business Simulator")
st.write("Adjust the sliders to see how business decisions impact financials.")

# Sidebar Inputs
st.sidebar.header("🔧 Adjust Business Variables")

utilization = st.sidebar.slider("Billable Utilization (%)", 50, 100, 75)
pricing = st.sidebar.slider("Average Pricing ($/hr)", 100, 500, 200)
staffing = st.sidebar.slider("Staffing (employees)", 5, 50, 10)
retention = st.sidebar.slider("Customer Retention (%)", 50, 100, 85)
pipeline = st.sidebar.slider("Sales Pipeline Coverage (x Revenue)", 1, 10, 3)
recurring_revenue = st.sidebar.slider("Recurring Revenue (%)", 0, 100, 50)
prime_contracts = st.sidebar.slider("Prime vs. Subcontractor Mix (%)", 0, 100, 70)
turnover = st.sidebar.slider("Employee Turnover Rate (%)", 0, 50, 10)
overhead_ratio = st.sidebar.slider("Billable vs. Overhead Staff Ratio (x)", 1, 10, 4)

# Business Logic Calculations
profit_margin = (utilization / 100) * pricing * staffing * (recurring_revenue / 100)
valuation = profit_margin * 5 * (retention / 100) * (prime_contracts / 100)

# Display Financial Projections
st.subheader("📈 Business Impact")
st.metric(label="Projected Profit Margin", value=f"${profit_margin:,.2f}K")
st.metric(label="Estimated Valuation", value=f"${valuation:,.2f}K")

# Simulated Growth Data
data = pd.DataFrame({
    "Timeframe": ["Now", "1 Year", "3 Years"],
    "Profit Margin ($K)": [profit_margin, profit_margin * 1.1, valuation],
})

# Chart Visualization
fig = px.line(data, x="Timeframe", y="Profit Margin ($K)", markers=True, title="Projected Financial Growth")
st.plotly_chart(fig)

# Conclusion
st.success("Adjust the sliders to see different business outcomes!")
