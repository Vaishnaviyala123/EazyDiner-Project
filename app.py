import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="EazyDiner Dashboard",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍽️ EazyDiner Bengaluru Restaurant Dashboard")

# Read the corrected CSV
df = pd.read_csv("EazyDiner_Cleaned.csv", encoding="utf-8-sig")

# Clean column names
df.columns = df.columns.str.strip()

# Convert numeric columns
for col in ["Price_for_Two", "Rating", "Review_Count",
            "Latitude", "Longitude"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Check required columns
required_columns = [
    "Restaurant_Name", "Location", "Cuisine",
    "Price_for_Two", "Rating", "Review_Count",
    "Address", "Phone_Number", "Latitude",
    "Longitude", "Opening_Hours", "URL"
]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    st.error(f"Missing columns: {missing}")
    st.stop()

# Dashboard metrics
st.success(f"Successfully loaded {len(df)} restaurants!")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Restaurants", len(df))
c2.metric("Average Price", f"₹{df['Price_for_Two'].mean():,.2f}")
c3.metric("Average Rating", f"{df['Rating'].mean():.2f} ⭐")
c4.metric("Total Reviews", f"{df['Review_Count'].sum():,.0f}")

# Charts
st.subheader("Top 10 Cuisines")
st.bar_chart(df["Cuisine"].value_counts().head(10))

st.subheader("Top 10 Locations")
st.bar_chart(df["Location"].value_counts().head(10))

st.subheader("Average Price by Cuisine")
st.bar_chart(
    df.groupby("Cuisine")["Price_for_Two"].mean().sort_values(ascending=False).head(10)
)

st.subheader("Restaurant Rating Distribution")
st.bar_chart(df["Rating"].value_counts().sort_index())

# Full dataset
st.subheader("Restaurant Details")
st.dataframe(df, use_container_width=True)
