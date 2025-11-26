import pandas as pd

INPUT_PATH = "./data_raw/median_income.csv"
OUTPUT_PATH = "./data_processed/median_income_clean.csv"

df = pd.read_csv(INPUT_PATH)
print("Raw shape:", df.shape)

# Drop unnamed metadata columns
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
print("After dropping Unnamed:", df.shape)

# Keep only census tracts
df = df[df["GEO_ID"].str.startswith("1400000US")].copy()
print("After keeping only tracts:", df.shape)

# Rename columns to friendlier names
df.rename(
    columns={
        "GEO_ID": "geoid",
        "NAME": "tract_name",
        "B19013_001E": "median_income",
    },
    inplace=True,
)

# make geoid format match other tables by removing leading "1400000US"
df["geoid"] = df["geoid"].str.replace("1400000US", "", regex=False)

# Keep only needed columns
df = df[["geoid", "tract_name", "median_income"]]

# Ensure numeric income
df["median_income"] = pd.to_numeric(df["median_income"], errors="coerce")

print("\n=== Preview of cleaned income data ===")
print(df.head())

df.to_csv(OUTPUT_PATH, index=False)
print("\nSaved cleaned file to:", OUTPUT_PATH)
