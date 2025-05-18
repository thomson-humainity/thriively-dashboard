import streamlit as st
from utils.data_loader import load_data, get_date_range, filter_data_by_date_range
from components.date_selector import init_date_selector_state, render_date_selector
from components.metrics import render_metrics
from components.charts import render_survey_chart

# Set page configuration
st.set_page_config(page_title="Survey Dashboard", page_icon="📊", layout="wide")

# Add a title
st.title("📊 Survey Dashboard")

# Create sidebar
st.sidebar.header("Settings")

# Load data and get date range
df = load_data()
FIRST_DATE, LAST_DATE = get_date_range(df)

# Initialize date selector state
init_date_selector_state(FIRST_DATE, LAST_DATE)

# Add some sample filters
st.sidebar.subheader("Filters")

# Get selected date range
date_range = render_date_selector(FIRST_DATE, LAST_DATE)

# Filter data based on date range
filtered_df = filter_data_by_date_range(df, date_range)

# Render metrics
render_metrics(filtered_df, df, date_range)

# Group by date and count surveys
daily_counts = filtered_df.groupby("survey_date").size().reset_index(name="count")

# Render chart
render_survey_chart(daily_counts)

# Add some sample text
st.markdown(
    """
### About this Dashboard
This dashboard displays historical survey data. Use the date range selector in the sidebar to filter the data.
"""
)
