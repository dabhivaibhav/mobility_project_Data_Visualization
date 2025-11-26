import pandas as pd

# File path
file_path = "./data_raw/travel_time.csv"

# Read raw file
df = pd.read_csv(file_path)
print("Raw shape:", df.shape)

# Drop any unnamed columns
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
print("After dropping Unnamed:", df.shape)

# Keep only census tracts (GEO_ID starting with 1400000US)
df = df[df["GEO_ID"].str.startswith("1400000US")].copy()
print("After keeping only tracts:", df.shape)

# Fix GEOID format to match other tables by removing leading "1400000US"
# Example: 1400000US17031010100 -> 17031010100
df["geoid"] = df["GEO_ID"].str.replace("1400000US", "", regex=False)

# Rename NAME -> tract_name
df.rename(columns={"NAME": "tract_name"}, inplace=True)

# Convert mean travel time to numeric (this is the total minutes value)
df["B08303_001E"] = pd.to_numeric(df["B08303_001E"], errors="coerce")

# Compute mean travel time in minutes
df["mean_travel_time_min"] = df["B08303_001E"] / 60.0

# Keep only what we need
df = df[["geoid", "tract_name", "mean_travel_time_min"]]

print("\n=== Preview of cleaned data ===")
print(df.head())

# Save
out_path = "./data_processed/travel_time_clean.csv"
df.to_csv(out_path, index=False)
print(f"\nSaved cleaned file to: {out_path}")
