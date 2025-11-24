import pandas as pd

# === Load cleaned files ===
income = pd.read_csv("./data_processed/median_income_clean.csv")
transport = pd.read_csv("./data_processed/means_transport_clean.csv")
vehicles = pd.read_csv("./data_processed/vehicles_available_clean.csv")
travel = pd.read_csv("./data_processed/travel_time_clean.csv")

print("Income rows:", len(income))
print("Transport rows:", len(transport))
print("Vehicles rows:", len(vehicles))
print("Travel rows:", len(travel))

# === Convert all geoids to strings ===
for df in [income, transport, vehicles, travel]:
    df["geoid"] = df["geoid"].astype(str)

# === Start master ===
master = income.copy()

# Don't duplicate tract_name during merges
master = master.merge(transport.drop(columns=["tract_name"]), on="geoid", how="left")

master = master.merge(vehicles.drop(columns=["tract_name"]), on="geoid", how="left")

master = master.merge(travel.drop(columns=["tract_name"]), on="geoid", how="left")

print("\nMaster shape:", master.shape)
print("\n=== Preview of master dataset ===")
print(master.head())

master.to_csv("./data_processed/tract_mobility_master.csv", index=False)
print("\nSaved master file to: ./data_processed/tract_mobility_master.csv")
