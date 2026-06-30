import pandas as pd

# Load the dataset
df = pd.read_csv("../data/myntra_products_raw.csv")
# Create an empty list to store categories
categories = []

# Go through every URL in the 'purl' column
for url in df["purl"]:

    # Split the URL at "myntra.com/"
    parts = url.split("myntra.com/")

    # Keep the part after "myntra.com/"
    remaining = parts[1]

    # Split again using "/" and take the first part
    category = remaining.split("/")[0]

    # Add the category to our list
    categories.append(category)

# Create a new column called "category"
df["category"] = categories

# Categories we want to keep
selected_categories = [
    "kurtas",
    "dresses",
    "tops",
    "jeans",
]

# Keep only rows whose category is in our list
filtered_df = df[df["category"].isin(selected_categories)]

# Show how many products are in each category
print("Products in each category:\n")
print(filtered_df["category"].value_counts())

# Show total number of products
print("\nTotal Products:", len(filtered_df))

# Save the filtered dataset
filtered_df.to_csv("../data/fashion_products.csv", index=False)
print("\nFiltered dataset saved successfully!")