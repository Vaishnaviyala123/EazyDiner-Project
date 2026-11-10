
import streamlit as st
import pandas as pd

st.set_page_config(page_title="EazyDiner Dashboard", layout="wide")

st.title("🍽️ EazyDiner Bengaluru Restaurant Dashboard")

df = pd.read_csv("EazyDiner_Cleaned (1).csv")
df.columns = df.columns.str.strip()

st.write("Actual column names:", [repr(col) for col in df.columns])

st.success(f"Dataset loaded successfully: {len(df)} restaurants")

st.metric("Total Restaurants", len(df))

c1, c2, c3 = st.columns(3)

c1.metric("Average Price for Two", f"₹{df['Price_for_Two'].mean():,.2f}")
c2.metric("Average Rating", f"{df['Rating'].mean():.2f} ⭐")
c3.metric("Total Reviews", f"{df['Review_Count'].sum():,.0f}")

st.subheader("Top 10 Restaurant Cuisines")
st.bar_chart(df["Cuisine"].value_counts().head(10))

st.subheader("Top 10 Restaurant Locations")
st.bar_chart(df["Location"].value_counts().head(10))

st.subheader("Restaurant Dataset")
st.dataframe(df, use_container_width=True)
