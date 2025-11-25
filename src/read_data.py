import pandas as pd

path = "./data_raw/means_transport.csv"

# skip metadata row
df = pd.read_csv(path, skiprows=1)

# drop useless "Unnamed" columns
df = df.loc[:, ~df.columns.str.contains("Unnamed")]

print("\n===== COLUMNS =====")
print(df.columns)

print("\n===== FIRST 10 ROWS =====")
print(df.head(10))

print("\nTotal rows:", len(df))
