import pandas as pd

path = "./data_raw/median_income.csv"

# Step 1: skip metadata row
df = pd.read_csv(path, skiprows=1)

# Step 2: drop useless "Unnamed" columns
df = df.loc[:, ~df.columns.str.contains("Unnamed")]

print("\n===== COLUMNS =====")
print(df.columns)

print("\n===== FIRST 10 ROWS =====")
print(df.head(10))

print("\nTotal rows:", len(df))
