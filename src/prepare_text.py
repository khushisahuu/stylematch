import pandas as pd

# Load the filtered dataset
df = pd.read_csv("../data/fashion_products.csv")
print("Original dataset size:", len(df))

# ---------------------------------------------------
# Remove duplicate products using product URL
# ---------------------------------------------------

df = df.drop_duplicates(subset="purl", keep="first")

print("After removing duplicate URLs:", len(df))

# ---------------------------------------------------
# Create combined text
# ---------------------------------------------------

df["combined_text"] = (
    df["name"] + " " +
    df["category"]
)

# ---------------------------------------------------
# Save prepared dataset
# ---------------------------------------------------

df.to_csv("../data/prepared_products.csv", index=False)
print("\nFirst 5 rows:\n")
print(df[["name", "combined_text"]].head())

print("\nPrepared dataset saved successfully!")