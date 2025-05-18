import streamlit as st
import plotly.express as px


def render_survey_chart(daily_counts):
    """Render the survey responses chart."""
    st.subheader("Survey Responses Over Time")
    fig = px.bar(daily_counts, x="survey_date", y="count", title="Daily Survey Count")
    fig.update_layout(
        yaxis_title="Number of Surveys", xaxis_title="Date", showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
