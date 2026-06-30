import streamlit as st
import pandas as pd
import requests
from recommender import get_recommendations

# ----------------------------
# Page Settings
# ----------------------------

st.set_page_config(
    page_title="StyleMatch | Fashion Recommender",
    page_icon="👗",
    layout="wide"
)

# ----------------------------
# Custom Styling
# ----------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0e0e10;
    color: #f5f5f5;
}

h1 {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-weight: 700;
    letter-spacing: -0.5px;
}

[data-testid="stCaptionContainer"] {
    color: #b3b3b3;
    font-size: 1.05rem;
}

div[data-baseweb="input"] { border-radius: 10px; }
div[data-baseweb="select"] { border-radius: 10px; }

div[data-testid="stImage"] img {
    border-radius: 14px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.35);
    width: 100%;
    object-fit: cover;
}

h3 {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    margin-top: 1.2rem;
}

hr { border-color: #2a2a2e !important; }

.product-card {
    background-color: #18181b;
    border: 1px solid #2a2a2e;
    border-radius: 16px;
    padding: 14px 14px 18px 14px;
    margin-bottom: 18px;
    transition: transform 0.15s ease, border-color 0.15s ease;
}

.product-card:hover {
    transform: translateY(-4px);
    border-color: #4a4a52;
}

.product-name {
    font-weight: 600;
    font-size: 1.02rem;
    margin-top: 10px;
    margin-bottom: 2px;
    color: #f5f5f5;
}

.product-brand {
    color: #9c9ca3;
    font-size: 0.85rem;
    margin-bottom: 8px;
}

.product-meta {
    font-size: 0.92rem;
    color: #d4d4d8;
    margin-bottom: 2px;
}

.match-badge {
    display: inline-block;
    background-color: #2e2e35;
    color: #c9c9ff;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 999px;
    margin-top: 8px;
    margin-bottom: 10px;
}

.stLinkButton a {
    border-radius: 8px !important;
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Image URL Helper
# ----------------------------
# The dataset stores multiple image URLs per product, separated by ";\n"
# (one per pixel-density variant: dpr_1.0, dpr_1.8, dpr_2.0, etc.)
# We extract just the first URL (dpr_1.0 = standard resolution).
# We also validate that the URL actually returns a 200 response before using it,
# falling back to a placeholder if it is missing, malformed, or broken.

PLACEHOLDER_IMG = "https://placehold.co/400x500?text=No+Image"

@st.cache_data(show_spinner=False, ttl=3600)
def safe_image_url(img_value):
    if img_value is None:
        return PLACEHOLDER_IMG

    img_str = str(img_value).strip()

    if img_str in ["", "-", "nan", "None"]:
        return PLACEHOLDER_IMG

    # Extract only the first URL from the semicolon-separated list
    first_url = img_str.split(";")[0].split("\n")[0].strip()

    if not first_url.startswith("http"):
        return PLACEHOLDER_IMG

    try:
        resp = requests.head(first_url, timeout=2)
        return first_url if resp.status_code == 200 else PLACEHOLDER_IMG
    except requests.RequestException:
        return PLACEHOLDER_IMG

# ----------------------------
# Load Dataset
# ----------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/prepared_products.csv")
df = load_data()

# ----------------------------
# Header
# ----------------------------

st.title("👗 StyleMatch — Fashion Recommender")
st.caption("Content-based fashion recommendation engine using TF-IDF and cosine similarity · Built on real Myntra product data")

st.divider()

# ----------------------------
# Search
# ----------------------------

search = st.text_input("🔎 Search for a product (e.g. 'embroidered top', 'skinny jeans', 'printed kurta')")

if search:

    matching = df[df["name"].str.contains(search, case=False, na=False)]

    if len(matching) == 0:
        st.warning("No products found. Try a different search term.")

    else:

        selected_product = st.selectbox(
            "Choose a product to get recommendations for:",
            matching["name"].unique()
        )

        selected = matching[matching["name"] == selected_product].iloc[0]

        st.divider()

        # ----------------------------
        # Selected Product
        # ----------------------------

        st.subheader("🖤 Selected Product")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(safe_image_url(selected["img"]), width=280)

        with col2:
            st.markdown(f"### {selected['name']}")
            st.write(f"**🏷 Brand:** {selected['seller']}")
            st.write(f"**📂 Category:** {selected['category'].capitalize()}")
            st.write(f"**💰 Price:** ₹{int(selected['price'])}")

            if pd.notna(selected["mrp"]) and selected["mrp"] > selected["price"]:
                discount = round(((selected["mrp"] - selected["price"]) / selected["mrp"]) * 100)
                st.write(f"**🏷 MRP:** ~~₹{int(selected['mrp'])}~~ &nbsp; 🟢 {discount}% off")

            if pd.notna(selected["rating"]) and selected["rating"] > 0:
                st.write(f"**⭐ Rating:** {selected['rating']} / 5")
            else:
                st.write("**⭐ Rating:** Not yet rated")

        st.divider()

        # ----------------------------
        # Recommendations
        # ----------------------------

        st.subheader("✨ You Might Like")

        with st.spinner("Finding similar products..."):
            recommendations = get_recommendations(selected_product)

        if not recommendations:
            st.info("No recommendations found for this product.")
        else:
            cols = st.columns(3)

            for i, product in enumerate(recommendations):

                with cols[i % 3]:

                    st.markdown('<div class="product-card">', unsafe_allow_html=True)

                    st.image(safe_image_url(product["Image"]), use_container_width=True)

                    st.markdown(f"""
                        <div class="product-name">{product['Name']}</div>
                        <div class="product-brand">{product['Brand']}</div>
                        <div class="product-meta">💰 {product['Price']}</div>
                        <div class="product-meta">⭐ {product['Rating']}</div>
                        <div class="match-badge">✦ {product['Similarity']} Match</div>
                    """, unsafe_allow_html=True)

                    st.link_button("View on Myntra ↗", product["URL"])

                    st.markdown('</div>', unsafe_allow_html=True)

        # ----------------------------
        # Footer
        # ----------------------------

        st.divider()
        st.caption("StyleMatch uses TF-IDF vectorization and cosine similarity to find products with similar names and categories. Built with Python, scikit-learn, pandas, and Streamlit.")

