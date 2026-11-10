import streamlit as st
import pandas as pd
import csv

st.set_page_config(
    page_title="EazyDiner Bengaluru Dashboard",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍽️ EazyDiner Bengaluru Restaurant Dashboard")
st.write("Restaurant Data Analysis Project")

# Load dataset
FILE_NAME = "EazyDiner_Cleaned (1).csv"

try:
    # Detect the CSV separator
    with open(FILE_NAME, "r", encoding="utf-8-sig", newline="") as file:
        sample = file.read(10000)
        file.seek(0)

        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
            separator = dialect.delimiter
        except csv.Error:
            separator = ","

    df = pd.read_csv(
        FILE_NAME,
        sep=separator,
        encoding="utf-8-sig",
        engine="python",
        on_bad_lines="warn"
    )

    # If still one column, try comma-separated parsing
    if len(df.columns) == 1:
        df = pd.read_csv(
            FILE_NAME,
            sep=",",
            encoding="utf-8-sig",
            engine="python"
        )

    # Clean column names
    df.columns = df.columns.astype(str).str.strip()

    # Expected dataset columns
    expected_columns = [
        "Restaurant_Name", "Location", "Cuisine",
        "Price_for_Two", "Rating", "Review_Count",
        "Address", "Phone_Number", "Latitude",
        "Longitude", "Opening_Hours", "URL"
    ]

    # Stop with a helpful message if columns are incorrect
    missing = [col for col in expected_columns if col not in df.columns]

    if missing:
        st.error("Some required columns are missing.")
        st.write("Detected columns:", df.columns.tolist())
        st.write("Missing columns:", missing)
        st.stop()

    # Convert numeric columns
    numeric_columns = [
        "Price_for_Two", "Rating", "Review_Count",
        "Latitude", "Longitude"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Dashboard metrics
    st.success(f"Dataset loaded successfully: {len(df)} restaurants")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Restaurants", len(df))
    col2.metric(
        "Average Price for Two",
        f"₹{df['Price_for_Two'].mean():,.2f}"
    )
    col3.metric(
        "Average Rating",
        f"{df['Rating'].mean():.2f} ⭐"
    )
    col4.metric(
        "Total Reviews",
        f"{df['Review_Count'].sum():,.0f}"
    )

    # Cuisine chart
    st.subheader("Top 10 Restaurant Cuisines")
    st.bar_chart(df["Cuisine"].value_counts().head(10))

    # Location chart
    st.subheader("Top 10 Restaurant Locations")
    st.bar_chart(df["Location"].value_counts().head(10))

    # Price chart
    st.subheader("Average Price by Cuisine")
    price_by_cuisine = (
        df.groupby("Cuisine")["Price_for_Two"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(price_by_cuisine)

    # Rating chart
    st.subheader("Restaurant Rating Distribution")
    st.bar_chart(df["Rating"].value_counts().sort_index())

    # Dataset
    st.subheader("Complete Restaurant Dataset")
    st.dataframe(df, use_container_width=True)

except FileNotFoundError:
    st.error(f"Dataset file not found: {FILE_NAME}")

except Exception as e:
    st.error("Something went wrong while loading the dashboard.")
    st.exception(e)
