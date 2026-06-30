import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

df = pd.read_csv("data/prepared_products.csv")
# --------------------------------------------------
# Create TF-IDF Matrix
# --------------------------------------------------

vectorizer = TfidfVectorizer(stop_words="english")

tfidf_matrix = vectorizer.fit_transform(df["combined_text"])

print("✅ Model Built Successfully!")
print("📦 Number of Products :", len(df))
print("📚 Vocabulary Size    :", tfidf_matrix.shape[1])


# --------------------------------------------------
# Recommendation Function
# --------------------------------------------------

def get_recommendations(product_name, top_n=5):

    matching_products = df[df["name"] == product_name]

    if len(matching_products) == 0:
        print("❌ Product not found!")
        return None

    product_index = matching_products.index[0]

    similarity_scores = cosine_similarity(
        tfidf_matrix[product_index],
        tfidf_matrix
    )

    scores = []

    for i in range(len(similarity_scores[0])):

        score = similarity_scores[0][i]

        scores.append((i, score))

    def get_score(item):
        return item[1]

    scores = sorted(scores, key=get_score, reverse=True)

    scores = scores[1:]

    recommendations = []

    seen_urls = set()

    for item in scores:

        index = item[0]
        similarity = item[1]

        product = df.iloc[index]

        if product["purl"] not in seen_urls:

            seen_urls.add(product["purl"])

            recommendations.append({
                "ID": product["id"],
                "Name": product["name"],
                "Brand": product["seller"],
                "Category": product["category"],
                "Price": f"₹{int(product['price'])}",
                "Rating": f"⭐ {product['rating']}",
                "Similarity": f"{round(similarity*100,2)}%",
                "Image": product["img"],
                "URL": product["purl"]
            })

        if len(recommendations) == top_n:
            break

    return recommendations


