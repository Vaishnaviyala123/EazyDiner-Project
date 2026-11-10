import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="EazyDiner Bengaluru Dashboard",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍽️ EazyDiner Bengaluru Restaurant Dashboard")
st.markdown("### Restaurant Data Analysis Project")

# --------------------------------
# 2. FIND THE CSV FILE
# --------------------------------

project_folder = Path(__file__).resolve().parent

csv_files = list(project_folder.glob("*.csv"))

if not csv_files:
    st.error("No CSV file found in your GitHub repository.")
    st.write("Available files:")
    st.write([file.name for file in project_folder.iterdir()])
    st.stop()

cleaned_files = [
    file for file in csv_files
    if "cleaned" in file.name.lower()
]

if not cleaned_files:
    st.error("Cleaned CSV file not found.")
    st.write("CSV files available:", [f.name for f in csv_files])
    st.stop()

file_path = next(
    (f for f in cleaned_files if f.name == "EazyDiner_Cleaned.csv"),
    cleaned_files[0]
)

st.caption(f"Dataset: {file_path.name}")

# --------------------------------
# 3. READ CSV WITH ENCODING FALLBACK
# --------------------------------

df = None

for encoding in ["utf-8-sig", "cp1252", "latin1"]:
    try:
        df = pd.read_csv(
            file_path,
            encoding=encoding,
            sep=",",
            engine="python",
            on_bad_lines="error"
        )
        st.success(f"Dataset loaded using {encoding} encoding.")
        break

    except UnicodeDecodeError:
        continue

    except Exception as error:
        st.error(f"CSV reading error: {error}")
        st.stop()

if df is None:
    st.error("Unable to read the CSV file.")
    st.stop()

# --------------------------------
# 4. CLEAN COLUMN NAMES
# --------------------------------

df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.strip('"')
    .str.strip("'")
)

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

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error("The CSV structure does not match the expected dataset.")
    st.write("Detected columns:", df.columns.tolist())
    st.write("Missing columns:", missing_columns)
    st.dataframe(df.head(5))
    st.stop()

# --------------------------------
# 5. DATA CLEANING
# --------------------------------

for col in [
    "Price_for_Two",
    "Rating",
    "Review_Count",
    "Latitude",
    "Longitude"
]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["Cuisine"] = df["Cuisine"].fillna("Unknown")
df["Location"] = df["Location"].fillna("Unknown")
df["Restaurant_Name"] = df["Restaurant_Name"].fillna("Unknown")

# --------------------------------
# 6. DASHBOARD METRICS
# --------------------------------

st.success(f"Successfully loaded {len(df)} restaurants!")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Restaurants",
    f"{len(df):,}"
)

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

st.divider()

# --------------------------------
# 7. CUISINE ANALYSIS
# --------------------------------

st.subheader("🍛 Top 10 Restaurant Cuisines")

cuisine_data = df["Cuisine"].value_counts().head(10)

st.bar_chart(cuisine_data)

# --------------------------------
# 8. LOCATION ANALYSIS
# --------------------------------

st.subheader("📍 Top 10 Restaurant Locations")

location_data = df["Location"].value_counts().head(10)

st.bar_chart(location_data)

# --------------------------------
# 9. PRICE ANALYSIS
# --------------------------------

st.subheader("💰 Average Price by Cuisine")

price_data = (
    df.groupby("Cuisine")["Price_for_Two"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(price_data)

# --------------------------------
# 10. RATING ANALYSIS
# --------------------------------

st.subheader("⭐ Restaurant Rating Distribution")

rating_data = df["Rating"].value_counts().sort_index()

st.bar_chart(rating_data)

# --------------------------------
# 11. RESTAURANT DETAILS
# --------------------------------

st.subheader("📋 Complete Restaurant Dataset")

search = st.text_input("Search restaurant by name")

if search:
    display_df = df[
        df["Restaurant_Name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]
else:
    display_df = df

st.dataframe(display_df, use_container_width=True)

st.caption("EazyDiner Bengaluru Restaurant Data Analysis Project")
