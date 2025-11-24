import pandas as pd

# Load raw data
path = "./data_raw/vehicles_available.csv"
df = pd.read_csv(path)

print("Raw shape:", df.shape)

# Drop empty unnamed columns
df = df.loc[:, ~df.columns.str.contains("Unnamed")]
print("After dropping Unnamed:", df.shape)

# Remove USA + metadata
df = df[df["GEO_ID"] != "Geography"].copy()
df = df[df["GEO_ID"] != "0100000US"].copy()
df = df[df["GEO_ID"].str.startswith("1400000US")].copy()
print("After keeping only tracts:", df.shape)

# Create clean GEOID
df["geoid"] = df["GEO_ID"].str.replace("1400000US", "", regex=False)

# Rename relevant fields
rename_map = {
    "NAME": "tract_name",
    "B08201_001E": "hh_total",
    "B08201_002E": "hh_no_vehicle",
    "B08201_003E": "hh_one_vehicle",
    "B08201_004E": "hh_two_vehicle",
    "B08201_005E": "hh_three_plus_vehicle",
}
df = df.rename(columns=rename_map)

cols_keep = [
    "geoid",
    "tract_name",
    "hh_total",
    "hh_no_vehicle",
    "hh_one_vehicle",
    "hh_two_vehicle",
    "hh_three_plus_vehicle",
]
df_clean = df[cols_keep].copy()

# convert to numeric
for col in [
    "hh_total",
    "hh_no_vehicle",
    "hh_one_vehicle",
    "hh_two_vehicle",
    "hh_three_plus_vehicle",
]:
    df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

# compute percentages
df_clean["pct_hh_no_vehicle"] = df_clean["hh_no_vehicle"] / df_clean["hh_total"]
df_clean["pct_hh_one_vehicle"] = df_clean["hh_one_vehicle"] / df_clean["hh_total"]
df_clean["pct_hh_two_vehicle"] = df_clean["hh_two_vehicle"] / df_clean["hh_total"]
df_clean["pct_hh_three_plus_vehicle"] = (
    df_clean["hh_three_plus_vehicle"] / df_clean["hh_total"]
)

# Save cleaned file
output = "./data_processed/vehicles_available_clean.csv"
df_clean.to_csv(output, index=False)

print("\n=== Preview of cleaned data ===")
print(df_clean.head())

print("\nSaved cleaned file:", output)
