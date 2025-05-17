import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# Add a title
st.title("📊 Dashboard")

# Create sidebar
st.sidebar.header("Settings")

# Sample data
@st.cache_data
def load_data():
    dates = pd.date_range(start='2024-01-01', end='2024-03-31', freq='D')
    data = pd.DataFrame({
        'date': dates,
        'value': np.random.normal(100, 15, len(dates))
    })
    return data

# Load data
df = load_data()

# Create two columns for metrics
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Average Value",
        value=f"${df['value'].mean():.2f}",
        delta=f"{df['value'].diff().mean():.2f}"
    )

with col2:
    st.metric(
        label="Total Records",
        value=len(df),
        delta=f"{len(df) - len(df.dropna())} missing"
    )

# Create a line chart
st.subheader("Value Over Time")
fig = px.line(df, x='date', y='value', title='Value Trend')
st.plotly_chart(fig, use_container_width=True)

# Add some sample filters
st.sidebar.subheader("Filters")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['date'].min(), df['date'].max())
)

# Add some sample text
st.markdown("""
### About this Dashboard
This is a sample dashboard created with Streamlit. You can modify this template to create your own custom dashboard.
""") 