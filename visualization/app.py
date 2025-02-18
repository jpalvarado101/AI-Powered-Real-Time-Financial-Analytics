import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Stock Market Analysis Dashboard")

# Load locally stored cleaned data (from ETL pipeline)
# Ensure the file 'stock_data_cleaned.parquet' exists from running etl_pipeline.py
df = pd.read_parquet("data/stock_data_cleaned.parquet")

# Convert timestamp to datetime if needed
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"])

st.subheader("Stock Prices Over Time")
fig = px.line(df, x="timestamp", y="close", color="ticker", title="Stock Prices")
st.plotly_chart(fig)
