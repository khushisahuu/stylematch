import pandas as pd
df = pd.read_csv("../data/myntra_products_raw.csv")
print(df.describe(include="all"))