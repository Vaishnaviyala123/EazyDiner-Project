
import streamlit as st
import pandas as pd
from pathlib import Path

# Page settings
st.set_page_config(
    page_title="EazyDiner Bengaluru Dashboard",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍽️ EazyDiner Bengaluru Restaurant Dashboard")
st.write("Restaurant Data Analysis Project")

# Find CSV files in the project folder
project_folder = Path(__file__).resolve().parent
csv_files = list(project_folder.glob("*.csv"))

if not csv_files:
    st.error("No CSV file found in the GitHub repository.")
    st.write("Available files:", [p.name for p in project_folder.iterdir()])
    st.stop()

# Prefer the cleaned dataset
cleaned_files = [
    f for f in csv_files
    if "cleaned" in f.name.lower()
]

if not cleaned_files:
    st.error("No cleaned CSV dataset found.")
    st.write("CSV files found:", [f.name for f in csv_files])
    st.stop()

# Prefer the exact filename, otherwise use the first cleaned file
file_path = next(
    (f for f in cleaned_files if f.name == "EazyDiner_Cleaned.csv"),
    cleaned_files[0]
)

st.caption(f"Dataset loaded from: {file_path.name}")

# Read the CSV file
try:
    df = pd.read_csv(file_path, encoding="utf-8-sig")
except Exception as error:
    st.error(f"Unable to read the CSV file: {error}")
    st.stop()

# Clean column names
df.columns = df.columns.astype(str).str.strip()

# Expected columns
required_columns = [
    "Restaurant_Name",
    "Location",
    "Cuisine",
    "Price_for_Two",
    "Rating",
    "Review_Count",
    "Address",
    "Phone_Number",
    "Latitude",
    "Longitude",
    "Opening_Hours",
    "URL"
]

# Validate dataset
missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error("Your CSV file is not correctly formatted.")
    st.write("Detected columns:", df.columns.tolist())
    st.write("Missing columns:", missing_columns)
    st.dataframe(df.head(5))
    st.stop()

# Convert numeric columns
numeric_columns = [
    "Price_for_Two",
    "Rating",
    "Review_Count",
    "Latitude",
    "Longitude"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Dashboard metrics
st.success(f"Successfully loaded {len(df)} restaurants!")

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

# Cuisine analysis
st.subheader("Top 10 Cuisines")
st.bar_chart(df["Cuisine"].value_counts().head(10))

# Location analysis
st.subheader("Top 10 Restaurant Locations")
st.bar_chart(df["Location"].value_counts().head(10))

# Price analysis
st.subheader("Average Price by Cuisine")

price_data = (
    df.groupby("Cuisine")["Price_for_Two"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(price_data)

# Rating analysis
st.subheader("Restaurant Rating Distribution")
st.bar_chart(df["Rating"].value_counts().sort_index())

# Restaurant data
st.subheader("Complete Restaurant Dataset")
st.dataframe(df, use_container_width=True)
