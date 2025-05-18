import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Survey Dashboard", page_icon="📊", layout="wide")

# Add a title
st.title("📊 Survey Dashboard")

# Create sidebar
st.sidebar.header("Settings")


# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/Final_Historical_Survey_Data.csv")
    # Convert date column to datetime
    df["survey_date"] = pd.to_datetime(df["survey_date"])
    return df


# Load data
df = load_data()

# Extract first and last dates and convert to Python datetime
FIRST_DATE = df["survey_date"].min().to_pydatetime()
LAST_DATE = df["survey_date"].max().to_pydatetime()

# Initialize session state for tracking last changed selector
if "last_changed" not in st.session_state:
    st.session_state.last_changed = "slider"
if "last_slider_value" not in st.session_state:
    st.session_state.last_slider_value = (FIRST_DATE, LAST_DATE)
if "last_input_value" not in st.session_state:
    st.session_state.last_input_value = (FIRST_DATE, LAST_DATE)

# Add some sample filters
st.sidebar.subheader("Filters")

# Date calendar input
date_calendar_range = st.sidebar.date_input(
    "Select Date Range", value=st.session_state.last_input_value
)

# Update last changed if calendar changed
if date_calendar_range != st.session_state.last_input_value:
    st.session_state.last_changed = "input"
    st.session_state.last_input_value = date_calendar_range

# Date slider with weekly steps
date_slider_range = st.sidebar.slider(
    "Select Date Range",
    min_value=FIRST_DATE,
    max_value=LAST_DATE,
    value=st.session_state.last_slider_value,
    step=pd.Timedelta(days=1),
    format="YYYY-MM-DD",
)

# Update last changed if slider changed
if date_slider_range != st.session_state.last_slider_value:
    st.session_state.last_changed = "slider"
    st.session_state.last_slider_value = date_slider_range

# Use the most recently changed selector
date_range = (
    date_slider_range
    if st.session_state.last_changed == "slider"
    else date_calendar_range
)

# Convert date_range to pandas datetime
date_range = [pd.to_datetime(d) for d in date_range]

# Filter data based on date range
filtered_df = df[df["survey_date"].between(date_range[0], date_range[1])]

# Create two columns for metrics
survey_count, survey_range = st.columns(2)

with survey_count:
    st.metric(
        label="Total Surveys",
        value=len(filtered_df),
        delta=f"{len(filtered_df) - len(df)} surveys omitted",
        border=True,
    )

with survey_range:
    st.metric(
        label="Date Range",
        value=f"{date_range[0].strftime('%Y-%m-%d')} - {date_range[1].strftime('%Y-%m-%d')} ({((date_range[1] - date_range[0]).days)} days)",
        delta=f"{(date_range[1] - date_range[0]).days} days included",
        border=True,
    )

# Group by date and count surveys
daily_counts = filtered_df.groupby("survey_date").size().reset_index(name="count")

# Create a bar chart
st.subheader("Survey Responses Over Time")
fig = px.bar(daily_counts, x="survey_date", y="count", title="Daily Survey Count")
fig.update_layout(yaxis_title="Number of Surveys", xaxis_title="Date", showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# Add some sample text
st.markdown(
    """
### About this Dashboard
This dashboard displays historical survey data. Use the date range selector in the sidebar to filter the data.
"""
)
