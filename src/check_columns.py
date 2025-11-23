import pandas as pd

df = pd.read_csv("./data_raw/means_transport.csv")
print(df.columns.tolist())
print(df.head())
