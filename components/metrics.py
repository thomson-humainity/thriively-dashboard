import streamlit as st


def render_metrics(filtered_df, df, date_range):
    """Render the metrics section of the dashboard."""
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
