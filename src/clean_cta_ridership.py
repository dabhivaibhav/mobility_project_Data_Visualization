import pandas as pd

file_path = "./data_raw/cta_entries.csv"

# Load raw data
df = pd.read_csv(file_path)
print("Raw shape:", df.shape)

# clean column names
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])

# convert rides to numeric
df["rides"] = pd.to_numeric(df["rides"], errors="coerce")
df = df.dropna(subset=["rides"])
df["rides"] = df["rides"].astype(int)

# filter to 2023 only
df = df[df["date"].dt.year == 2023]
print("After filtering 2023:", df.shape)


# Rename Station Name column

df.rename(columns={"stationname": "station_name"}, inplace=True)


# Aggregate to get total rides, avg daily, avg weekday, avg weekend
def avg_weekday(group):
    return group[group["daytype"] == "W"]["rides"].mean()


def avg_weekend(group):
    return group[group["daytype"].isin(["A", "U"])]["rides"].mean()


agg = (
    df.groupby(["station_id", "station_name"])
    .apply(
        lambda g: pd.Series(
            {
                "total_rides": g["rides"].sum(),
                "avg_rides_daily": g["rides"].mean(),
                "avg_weekday": avg_weekday(g),
                "avg_weekend": avg_weekend(g),
            }
        )
    )
    .reset_index()
)


# OUTPUT
print("\n=== PREVIEW OF CLEANED DATA ===")
print(agg.head())
print(f"\nStations processed: {agg.shape[0]}")

# Save cleaned file
agg.to_csv("./data_processed/cta_ridership_clean.csv", index=False)
print("\nSaved cleaned file to: ./data_processed/cta_ridership_clean.csv")
