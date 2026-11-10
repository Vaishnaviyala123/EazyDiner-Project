import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="EazyDiner Dashboard",
    layout="wide"
)

st.title("🍽️ EazyDiner Bengaluru Restaurant Dashboard")

# Read CSV file
df = pd.read_csv(
    "EazyDiner_Cleaned (1).csv",
    sep=",",
    encoding="utf-8-sig"
)

# Clean column names
df.columns = df.columns.str.strip()

# Fix if the CSV was saved with all columns in one field
if len(df.columns) == 1 and "," in df.columns[0]:
    df = df.iloc[:, 0].str.split(",", expand=True)
    df.columns = [
        "Restaurant_Name", "Location", "Cuisine",
        "Price_for_Two", "Rating", "Review_Count",
        "Address", "Phone_Number", "Latitude",
        "Longitude", "Opening_Hours", "URL"
    ]

# Convert numeric columns
for col in ["Price_for_Two", "Rating", "Review_Count"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

st.success(f"Dataset loaded: {len(df)} restaurants")

c1, c2, c3 = st.columns(3)

c1.metric("Total Restaurants", len(df))
c2.metric("Average Price for Two", f"₹{df['Price_for_Two'].mean():,.2f}")
c3.metric("Average Rating", f"{df['Rating'].mean():.2f} ⭐")

st.metric("Total Reviews", f"{df['Review_Count'].sum():,.0f}")

st.subheader("Top 10 Restaurant Cuisines")
st.bar_chart(df["Cuisine"].value_counts().head(10))

st.subheader("Top 10 Restaurant Locations")
st.bar_chart(df["Location"].value_counts().head(10))

st.subheader("Restaurant Dataset")
st.dataframe(df, use_container_width=True)

