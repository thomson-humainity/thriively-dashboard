import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


def init_filter_state(first_date, last_date):
    """Initialize the filter state with default values."""
    # Date selector state
    if "last_changed" not in st.session_state:
        st.session_state.last_changed = "slider"
    if "last_slider_value" not in st.session_state:
        st.session_state.last_slider_value = (first_date, last_date)
    if "last_input_value" not in st.session_state:
        st.session_state.last_input_value = (first_date, last_date)

    # Team and department state
    if "selected_teams" not in st.session_state:
        st.session_state.selected_teams = []
    if "selected_departments" not in st.session_state:
        st.session_state.selected_departments = []


def render_filters(df):
    """Render all filters in the sidebar."""
    st.sidebar.header("Filters")

    # Date Range Filter
    st.sidebar.subheader("Date Range")
    date_range = render_date_selector(df["survey_date"].min(), df["survey_date"].max())

    # Department Filter
    st.sidebar.subheader("Departments")
    all_departments = sorted(df["department"].unique())
    selected_departments = st.sidebar.multiselect(
        "Select Departments",
        options=all_departments,
        default=st.session_state.selected_departments,
        key="department_filter",
    )
    st.session_state.selected_departments = selected_departments

    # Team Filter
    st.sidebar.subheader("Teams")
    all_teams = sorted(df["team"].unique())
    selected_teams = st.sidebar.multiselect(
        "Select Teams",
        options=all_teams,
        default=st.session_state.selected_teams,
        key="team_filter",
    )
    st.session_state.selected_teams = selected_teams

    return date_range, selected_teams, selected_departments


def render_date_selector(first_date, last_date):
    """Render the date selection components and return the selected range."""
    # Date calendar input
    date_calendar_range = st.sidebar.date_input(
        "Select Date Range",
        value=st.session_state.last_input_value,
        key="date_calendar",
    )

    # Update last changed if calendar changed
    if date_calendar_range != st.session_state.last_input_value:
        st.session_state.last_changed = "input"
        st.session_state.last_input_value = date_calendar_range

    # Date slider with daily steps
    date_slider_range = st.sidebar.slider(
        "Select Date Range",
        min_value=first_date,
        max_value=last_date,
        value=st.session_state.last_slider_value,
        step=pd.Timedelta(days=1),
        format="YYYY-MM-DD",
        key="date_slider",
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

    # Convert to pandas datetime
    return [pd.to_datetime(d) for d in date_range]
