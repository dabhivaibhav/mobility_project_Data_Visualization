import pandas as pd

# 1. Read the master dataset
file_path = "./data_processed/tract_mobility_master.csv"
df = pd.read_csv(file_path)

print("=== BASIC INFO ===")
print("Shape (rows, columns):", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\n=== FIRST 5 ROWS ===")
print(df.head())

print("\n=== SUMMARY STATS (numeric) ===")
print(df.describe())

print("\n=== MISSING VALUES PER COLUMN ===")
print(df.isna().sum())
