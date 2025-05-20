import streamlit as st
import plotly.express as px


def render_scores_metrics(filtered_df):
    """Render the metrics section for all scores."""
    # Compute overall averages for each score column
    overall_averages = filtered_df[
        [
            "psychological_safety",
            "dependability",
            "clarity",
            "meaning",
            "impact",
            "communication",
            "collaboration",
            "innovation",
            "engagement_score",
        ]
    ].mean()

    # Create a 3x3 grid of metrics
    st.subheader("Overall Metrics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="🛡️ Psychological Safety",
            value=f"{overall_averages['psychological_safety']:.1f}",
        )
        st.metric(
            label="🤝 Dependability", value=f"{overall_averages['dependability']:.1f}"
        )
        st.metric(label="🎯 Clarity", value=f"{overall_averages['clarity']:.1f}")

    with col2:
        st.metric(label="💫 Meaning", value=f"{overall_averages['meaning']:.1f}")
        st.metric(label="✨ Impact", value=f"{overall_averages['impact']:.1f}")
        st.metric(
            label="💬 Communication", value=f"{overall_averages['communication']:.1f}"
        )

    with col3:
        st.metric(
            label="👥 Collaboration", value=f"{overall_averages['collaboration']:.1f}"
        )
        st.metric(label="💡 Innovation", value=f"{overall_averages['innovation']:.1f}")
        st.metric(
            label="📈 Engagement Score",
            value=f"{overall_averages['engagement_score']:.1f}",
        )


def render_scores_chart(filtered_df):
    """Render the line chart showing scores over time."""
    # Group by date and average score columns
    daily_averages = (
        filtered_df.groupby("survey_date")[
            [
                "psychological_safety",
                "dependability",
                "clarity",
                "meaning",
                "impact",
                "communication",
                "collaboration",
                "innovation",
                "engagement_score",
            ]
        ]
        .mean()
        .reset_index()
    )

    # Create the line chart
    fig = px.line(
        daily_averages,
        x="survey_date",
        y=[
            "psychological_safety",
            "dependability",
            "clarity",
            "meaning",
            "impact",
            "communication",
            "collaboration",
            "innovation",
            "engagement_score",
        ],
        title="Survey Metrics Over Time",
    )

    # Update layout to move legend to the right
    fig.update_layout(
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=1.05),
        margin=dict(r=150),  # Add margin on the right for the legend
    )

    st.plotly_chart(fig, use_container_width=True)
