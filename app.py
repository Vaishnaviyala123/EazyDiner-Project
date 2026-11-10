import streamlit as st
import pandas as pd
import csv

st.set_page_config(
    page_title="EazyDiner Restaurant Dashboard",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍽️ EazyDiner Bengaluru Restaurant Dashboard")
st.write("Restaurant Data Analysis Project")

# Load CSV file
FILE_NAME = "EazyDiner_Cleaned (1).csv"

try:
    df = pd.read_csv(
        FILE_NAME,
        encoding="utf-8-sig",
        sep=",",
        engine="python",
        quoting=csv.QUOTE_NONE
    )

    # Clean column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.strip('"')
        .str.strip("'")
    )

    # Display dataset information
    st.write("Number of columns:", len(df.columns))
    st.write("Column names:", df.columns.tolist())

    # Required columns
    required_columns = [
        "Restaurant_Name", "Location", "Cuisine",
        "Price_for_Two", "Rating", "Review_Count",
        "Address", "Phone_Number", "Latitude",
        "Longitude", "Opening_Hours", "URL"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        st.error("CSV format is incorrect. Please check the dataset file.")
        st.write("Missing columns:", missing_columns)
        st.stop()

    # Convert numeric columns
    for col in [
        "Price_for_Two", "Rating", "Review_Count",
        "Latitude", "Longitude"
    ]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Dashboard metrics
    st.success(f"Successfully loaded {len(df)} restaurants!")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Restaurants", len(df))
    c2.metric(
        "Average Price for Two",
        f"₹{df['Price_for_Two'].mean():,.2f}"
    )
    c3.metric(
        "Average Rating",
        f"{df['Rating'].mean():.2f} ⭐"
    )
    c4.metric(
        "Total Reviews",
        f"{df['Review_Count'].sum():,.0f}"
    )

    # Charts
    st.subheader("Top 10 Cuisines")
    st.bar_chart(df["Cuisine"].value_counts().head(10))

    st.subheader("Top 10 Locations")
    st.bar_chart(df["Location"].value_counts().head(10))

    st.subheader("Average Price by Cuisine")
    price_data = (
        df.groupby("Cuisine")["Price_for_Two"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(price_data)

    st.subheader("Restaurant Rating Distribution")
    st.bar_chart(df["Rating"].value_counts().sort_index())

    # Full dataset
    st.subheader("Restaurant Details")
    st.dataframe(df, use_container_width=True)

except FileNotFoundError:
    st.error(f"File not found: {FILE_NAME}. Check the filename in GitHub.")

except Exception as e:
    st.error(f"Error: {e}")
