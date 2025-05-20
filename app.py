import streamlit as st
from utils.data_loader import load_data, get_date_range, filter_data_by_date_range
from components.filters import init_filter_state, render_filters
from components.metrics import render_metrics
from components.charts import render_survey_chart
from components.scores import render_scores_metrics, render_scores_chart

#################
### PAGE SETUP ###
#################

# Set page configuration
st.set_page_config(page_title="Survey Dashboard", page_icon="📊", layout="wide")

# Add a title
st.title("📊 Survey Dashboard")

#################
### PAGE FILTERS ###
#################

# Load data and get date range
df = load_data()
FIRST_DATE, LAST_DATE = get_date_range(df)

# Initialize filter state
init_filter_state(FIRST_DATE, LAST_DATE)

# Render all filters and get selected values
date_range, selected_teams, selected_departments = render_filters(df)

# Filter data based on all filters
filtered_df = df.copy()

# Apply date range filter
filtered_df = filter_data_by_date_range(filtered_df, date_range)

# Apply team filter if any teams are selected
if selected_teams:
    filtered_df = filtered_df[filtered_df["team"].isin(selected_teams)]

# Apply department filter if any departments are selected
if selected_departments:
    filtered_df = filtered_df[filtered_df["department"].isin(selected_departments)]

#################
### PAGE METRICS ###
#################

# Render metrics
render_metrics(filtered_df, df, date_range)

#################
### PAGE CHARTS ###
#################

# Group by date and count surveys
daily_counts = filtered_df.groupby("survey_date").size().reset_index(name="count")

# Render chart
render_survey_chart(daily_counts)

#################
### PAGE SCORES ###
#################

# Render scores metrics and chart
render_scores_metrics(filtered_df)
render_scores_chart(filtered_df)

#################
### PAGE TEXT ###
#################

# display the filtered df in the streamlit app
st.dataframe(filtered_df)

st.markdown(filtered_df.columns)

# Add some sample text
st.markdown(
    """
### About this Dashboard
This dashboard displays historical survey data. Use the filters in the sidebar to filter the data by date range, team, and department.
"""
)
