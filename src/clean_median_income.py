import pandas as pd

# Load raw CSV file
path = "./data_raw/median_income.csv"

df = pd.read_csv(path, skiprows=1)

print("Raw shape:", df.shape)

# Rename columns to simpler names for easier handling
df = df.rename(
    columns={
        "Geography": "geoid_raw",
        "Geographic Area Name": "tract_name",
        "Estimate!!Median household income in the past 12 months (in 2023 inflation-adjusted dollars)": "median_income",
        "Margin of Error!!Median household income in the past 12 months (in 2023 inflation-adjusted dollars)": "median_income_moe",
    }
)

# Keep only census tracts
# In this file, tract rows start with '1400000US'
df = df[df["geoid_raw"].str.startswith("1400000US")].copy()

print("After keeping only tracts:", df.shape)

# Extract clean GEOID
# Remove the '1400000US' prefix so we just have the 11-digit tract ID
df["geoid"] = df["geoid_raw"].str.replace("1400000US", "", regex=False)

# Convert income to numeric
df["median_income"] = pd.to_numeric(df["median_income"], errors="coerce")

# Keep only the columns we care about
df_clean = df[["geoid", "tract_name", "median_income"]].copy()

print("\n=== Preview of cleaned data ===")
print(df_clean.head())
print("\nNumber of cleaned tracts:", len(df_clean))

# Save cleaned file to data_processed folder
output_path = "./data_processed/median_income_clean.csv"
df_clean.to_csv(output_path, index=False)

print("\nSaved cleaned file to:", output_path)
