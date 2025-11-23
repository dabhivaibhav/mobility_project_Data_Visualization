import pandas as pd

# Load raw file
path = "./data_raw/means_transport.csv"
df = pd.read_csv(path)

print("Raw shape:", df.shape)

# Drop the Unnamed column at the end
df = df.loc[:, ~df.columns.str.contains("Unnamed")]
print("After dropping Unnamed:", df.shape)

# Remove non-tract rows
# Row 0 is "Geography", row 1 is "0100000US" (USA)
df = df[df["GEO_ID"] != "Geography"].copy()
df = df[df["GEO_ID"] != "0100000US"].copy()

# keeping only census tracts (IDs that start with 1400000US...)
df = df[df["GEO_ID"].str.startswith("1400000US")].copy()
print("After keeping only tracts:", df.shape)

# Clean GEOID
df["geoid"] = df["GEO_ID"].str.replace("1400000US", "", regex=False)

# Rename important columns to readable names
rename_map = {
    "NAME": "tract_name",
    "B08301_001E": "workers_total",
    "B08301_002E": "workers_car",
    "B08301_010E": "workers_public",
    "B08301_018E": "workers_walk",
    "B08301_019E": "workers_other",
    "B08301_021E": "workers_home",
}
df = df.rename(columns=rename_map)

# Keep only the columns we care abou
cols_keep = [
    "geoid",
    "tract_name",
    "workers_total",
    "workers_car",
    "workers_public",
    "workers_walk",
    "workers_other",
    "workers_home",
]
df_clean = df[cols_keep].copy()

# Ensure counts are numeric
for col in [
    "workers_total",
    "workers_car",
    "workers_public",
    "workers_walk",
    "workers_other",
    "workers_home",
]:
    df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

# Compute percentages (mode shares) for each transport mode
df_clean["pct_car"] = df_clean["workers_car"] / df_clean["workers_total"]
df_clean["pct_public"] = df_clean["workers_public"] / df_clean["workers_total"]
df_clean["pct_walk"] = df_clean["workers_walk"] / df_clean["workers_total"]
df_clean["pct_other"] = df_clean["workers_other"] / df_clean["workers_total"]
df_clean["pct_home"] = df_clean["workers_home"] / df_clean["workers_total"]

# Save cleaned file
output = "./data_processed/means_transport_clean.csv"
df_clean.to_csv(output, index=False)

print("\n=== Preview of cleaned data ===")
print(df_clean.head())

print("\nSaved cleaned file:", output)
