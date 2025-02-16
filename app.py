import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Set page title
st.set_page_config(page_title="Digital Twin Business Simulator", layout="wide")

# Title and Description
st.title("🛩️ Digital Twin Business Simulator")
st.write("Adjust the sliders to see how business decisions impact financials.")

# Sidebar Inputs
st.sidebar.header("🔧 Adjust Business Variables")

# Industry Selection Dropdown
industry_options = {
    "Consulting": "Consulting",
    "Government Contracting": "Government",
    "IT Services": "Technology",
    "Healthcare": "Healthcare",
    "Finance": "Finance",
}

selected_industry = st.sidebar.selectbox("Select Industry", list(industry_options.keys()))

utilization = st.sidebar.slider("Billable Utilization (%)", 50, 100, 75)
staffing = st.sidebar.slider("Staffing (employees)", 5, 50, 10)
retention = st.sidebar.slider("Customer Retention (%)", 50, 100, 85)
pipeline = st.sidebar.slider("Sales Pipeline Coverage (x Revenue)", 1, 10, 3)
recurring_revenue = st.sidebar.slider("Recurring Revenue (%)", 0, 100, 50)
prime_contracts = st.sidebar.slider("Prime vs. Subcontractor Mix (%)", 0, 100, 70)
turnover = st.sidebar.slider("Employee Turnover Rate (%)", 0, 50, 10)
overhead_ratio = st.sidebar.slider("Billable vs. Overhead Staff Ratio (x)", 1, 10, 4)

# Function to fetch competitive pricing data based on industry
def get_competitive_pricing(industry):
    industry_pricing_defaults = {
        "Consulting": 200,
        "Government": 150,
        "Technology": 250,
        "Healthcare": 180,
        "Finance": 220,
    }
    
    try:
        headers = {"User-Agent": "your-email@example.com", "Accept": "application/json"}
        response = requests.get(f"https://api.bls.gov/public/pricing?industry={industry}", headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data.get("average_hourly_rate", industry_pricing_defaults.get(industry, 150))  # Fallback to static default
        else:
            st.warning(f"Pricing API Error: {response.status_code} - Using fallback pricing")
    except Exception as e:
        st.warning(f"Using default pricing due to API error: {str(e)}")

    return industry_pricing_defaults.get(industry, 150)  # Default fallback value

# Fetch real-time pricing based on selected industry
industry_code = industry_options[selected_industry]
competitive_pricing = get_competitive_pricing(industry_code)

# Pricing slider with dynamic industry data
pricing = st.sidebar.slider("Average Pricing ($/hr)", 50, 500, int(competitive_pricing))

# Business Logic Calculations
profit_margin = (utilization / 100) * pricing * staffing * (recurring_revenue / 100) * 0.2
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
