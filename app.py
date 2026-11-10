# Load dataset
FILE_NAME = "EazyDiner_Cleaned (1).csv"

df = pd.read_csv(
    FILE_NAME,
    sep=",",
    encoding="utf-8-sig",
    engine="python",
    quoting=csv.QUOTE_NONE
)

# Remove unwanted quote characters
df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.strip('"')
    .str.strip("'")
)

st.write("Detected number of columns:", len(df.columns))
st.write("Detected column names:", df.columns.tolist())
st.write("First 3 rows:", df.head(3))
