import streamlit as st
import pandas as pd
from pathlib import Path

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="EazyDiner - Find Restaurants",
    page_icon="🍽️",
    layout="wide"
)

# -----------------------------------
# CUSTOM DESIGN
# -----------------------------------

st.markdown("""
<style>
.main {
    background-color: #fffaf5;
}
.hero {
    background: linear-gradient(120deg, #702323, #bd633d);
    padding: 35px;
    border-radius: 15px;
    color: white;
    text-align: center;
}
.hero h1 {
    color: white;
}
.restaurant-card {
    background: white;
    padding: 18px;
    border: 1px solid #eee0d8;
    border-radius: 14px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# LOAD DATASET
# -----------------------------------

folder = Path(__file__).resolve().parent

files = list(folder.glob("*Cleaned*.csv"))

if not files:
    st.error("Restaurant CSV file not found in the repository.")
    st.stop()

file_path = files[0]
df = None

for encoding in ["utf-8-sig", "cp1252", "latin1"]:
    try:
        df = pd.read_csv(file_path, encoding=encoding)
        break
    except UnicodeDecodeError:
        continue

if df is None:
    st.error("Unable to read the restaurant dataset.")
    st.stop()

df.columns = df.columns.astype(str).str.strip()

required = [
    "Restaurant_Name", "Location", "Cuisine",
    "Price_for_Two", "Rating", "Review_Count",
    "Address", "Phone_Number", "URL"
]

missing = [col for col in required if col not in df.columns]

if missing:
    st.error(f"Missing dataset columns: {missing}")
    st.stop()

# Clean data
for col in ["Price_for_Two", "Rating", "Review_Count"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["Restaurant_Name"] = df["Restaurant_Name"].fillna("Restaurant")
df["Location"] = df["Location"].fillna("Unknown")
df["Cuisine"] = df["Cuisine"].fillna("Not specified")

# -----------------------------------
# HEADER
# -----------------------------------

st.markdown("""
<div class="hero">
    <h1>🍽️ EazyDiner</h1>
    <h3>Discover the best restaurants in Bengaluru</h3>
    <p>Explore restaurants, cuisines, ratings and dining options.</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# -----------------------------------
# SEARCH AND FILTERS
# -----------------------------------

st.subheader("Find Your Restaurant")

search = st.text_input(
    "🔍 Search restaurant",
    placeholder="Enter restaurant name..."
)

locations = ["All Locations"] + sorted(
    df["Location"].dropna().astype(str).unique().tolist()
)

cuisines = ["All Cuisines"] + sorted(
    df["Cuisine"].dropna().astype(str).unique().tolist()
)

col1, col2, col3 = st.columns(3)

with col1:
    selected_location = st.selectbox(
        "Choose Location", locations
    )

with col2:
    selected_cuisine = st.selectbox(
        "Choose Cuisine", cuisines
    )

with col3:
    sort_option = st.selectbox(
        "Sort Restaurants",
        ["Recommended", "Highest Rating", "Lowest Price"]
    )

# -----------------------------------
# FILTER DATA
# -----------------------------------

filtered = df.copy()

if search:
    filtered = filtered[
        filtered["Restaurant_Name"].astype(str).str.contains(
            search, case=False, na=False
        )
    ]

if selected_location != "All Locations":
    filtered = filtered[
        filtered["Location"] == selected_location
    ]

if selected_cuisine != "All Cuisines":
    filtered = filtered[
        filtered["Cuisine"] == selected_cuisine
    ]

if sort_option == "Highest Rating":
    filtered = filtered.sort_values(
        "Rating", ascending=False, na_position="last"
    )

elif sort_option == "Lowest Price":
    filtered = filtered.sort_values(
        "Price_for_Two", ascending=True, na_position="last"
    )

st.write(f"### {len(filtered)} Restaurants Found")

# -----------------------------------
# RESTAURANT LISTINGS
# -----------------------------------

if filtered.empty:
    st.warning("No restaurants found. Try different search filters.")

else:
    for start in range(0, len(filtered), 2):
        cols = st.columns(2)

        for offset, col in enumerate(cols):
            index = start + offset

            if index >= len(filtered):
                break

            restaurant = filtered.iloc[index]

            with col:
                with st.container(border=True):

                    st.subheader(
                        f"🍴 {restaurant['Restaurant_Name']}"
                    )

                    rating = restaurant["Rating"]

                    if pd.notna(rating):
                        st.write(f"⭐ Rating: {rating:.1f}/5")
                    else:
                        st.write("⭐ Rating not available")

                    st.write(f"📍 {restaurant['Location']}")
                    st.write(f"🍛 {restaurant['Cuisine']}")

                    price = restaurant["Price_for_Two"]

                    if pd.notna(price):
                        st.write(f"💰 ₹{price:,.0f} for two")
                    else:
                        st.write("Price not available")

                    st.write(f"📌 {restaurant['Address']}")

                    url = restaurant["URL"]

                    if pd.notna(url) and str(url).strip().startswith("https://"):
                        st.link_button(
                            "View Restaurant / Menu / Booking",
                            str(url).strip(),
                            use_container_width=True
                        )
                    elif pd.notna(url) and str(url).strip().startswith("http://"):
                        st.link_button(
                            "View Restaurant / Menu / Booking",
                            str(url).strip(),
                            use_container_width=True
                        )
                    else:
                        st.caption("Restaurant booking link unavailable.")

# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.markdown("""
<center>
<h3>🍽️ EazyDiner Bengaluru</h3>
<p>Discover restaurants and explore dining options.</p>
<p>Web Scraping and Data Analysis Project</p>
</center>
""", unsafe_allow_html=True)
