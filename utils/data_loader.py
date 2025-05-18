import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    """Load and preprocess the survey data."""
    df = pd.read_csv("data/Final_Historical_Survey_Data.csv")
    # Convert date column to datetime
    df["survey_date"] = pd.to_datetime(df["survey_date"])
    return df


def get_date_range(df):
    """Get the first and last dates from the dataset."""
    first_date = df["survey_date"].min().to_pydatetime()
    last_date = df["survey_date"].max().to_pydatetime()
    return first_date, last_date


def filter_data_by_date_range(df, date_range):
    """Filter the dataframe by the given date range."""
    return df[df["survey_date"].between(date_range[0], date_range[1])]
