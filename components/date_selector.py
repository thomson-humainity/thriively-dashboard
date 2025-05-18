import streamlit as st
import pandas as pd


def init_date_selector_state(first_date, last_date):
    """Initialize the session state for date selection."""
    if "last_changed" not in st.session_state:
        st.session_state.last_changed = "slider"
    if "last_slider_value" not in st.session_state:
        st.session_state.last_slider_value = (first_date, last_date)
    if "last_input_value" not in st.session_state:
        st.session_state.last_input_value = (first_date, last_date)


def render_date_selector(first_date, last_date):
    """Render the date selection components and return the selected range."""
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
        min_value=first_date,
        max_value=last_date,
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

    # Convert to pandas datetime
    return [pd.to_datetime(d) for d in date_range]
