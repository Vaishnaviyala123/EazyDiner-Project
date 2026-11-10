import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="EazyDiner Dashboard", layout="wide")

st.title("🍽️ EazyDiner Bengaluru Restaurant Dashboard")

df = pd.read_csv("EazyDiner_Cleaned.csv")

st.metric("Total Restaurants", len(df))

c1, c2, c3 = st.columns(3)
c1.metric("Average Price for Two", f"₹{df['Price_for_Two'].mean():,.2f}")
c2.metric("Average Rating", f"{df['Rating'].mean():.2f} ⭐")
c3.metric("Total Reviews", f"{df['Review_Count'].sum():,.0f}")

st.subheader("Top 10 Restaurant Cuisines")
fig, ax = plt.subplots()
df["Cuisine"].value_counts().head(10).plot(kind="bar", ax=ax)
st.pyplot(fig)
plt.close(fig)

st.subheader("Top 10 Restaurant Locations")
fig, ax = plt.subplots()
df["Location"].value_counts().head(10).plot(kind="bar", ax=ax)
st.pyplot(fig)
plt.close(fig)

st.subheader("Restaurant Dataset")
st.dataframe(df, use_container_width=True)
