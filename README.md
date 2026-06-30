# 👗 StyleMatch — Fashion Recommendation Engine

A content-based fashion product recommendation system built using **NLP (TF-IDF)** and **cosine similarity**, trained on real Myntra product data.

Given any fashion product, StyleMatch finds the most similar alternatives — by product name and category — and displays them in a clean, interactive web interface.

---

## 🛠 Tech Stack

- **Python** — core language
- **pandas** — data loading, cleaning, and preprocessing
- **scikit-learn** — TF-IDF vectorization and cosine similarity
- **Streamlit** — interactive web frontend
- **Kaggle Dataset** — real Myntra fashion product data (~76,000 products after cleaning)

---

## 📁 Project Structure

```
stylematch/
│
├── data/
│   ├── myntra_products_raw.csv       # Original downloaded dataset (not pushed to GitHub — too large)
│   ├── fashion_products.csv          # After category filtering
│   └── prepared_products.csv         # Final cleaned dataset used by the app
│
├── notebooks/
│   └── exploration.ipynb             # Initial data exploration (optional)
│
├── src/
│   ├── filter_data.py                # Step 1: extract category from URL, filter to 4 categories
│   ├── prepare_text.py               # Step 2: combine text features for TF-IDF
│   └── build_model.py                # Step 3: TF-IDF vectorizer + recommendation logic test
│
├── recommender.py                    # Core recommendation engine (imported by app)
├── app.py                            # Streamlit frontend
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Excludes large CSV files and venv
└── README.md
```

---

## ⚙️ How It Works

1. **Data Preprocessing** — filtered 1M+ raw Myntra products to 4 focused categories (kurtas, dresses, tops, jeans). Removed ~10,000 duplicate product URLs using `drop_duplicates(subset="purl")`.

2. **Feature Engineering** — combined `name` and `category` into a single `combined_text` field. Deliberately excluded `seller` after observing it biased recommendations toward same-brand products.

3. **TF-IDF Vectorization** — `TfidfVectorizer` converts product text into numeric vectors, weighting rare descriptive words higher and ignoring common English stop words.

4. **Cosine Similarity** — instead of pre-computing an 86k×86k similarity matrix (which would require ~60GB RAM), similarity is computed **on-demand** for the selected product only — a deliberate memory optimization.

5. **Streamlit UI** — search, select a product, and browse recommendations with images, prices, ratings, and direct Myntra links.

---

## 🚀 Running Locally

```bash
# Clone the repository
git clone https://github.com/khushisahuu/stylematch.git
cd stylematch

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

> **Note:** The raw dataset is too large for GitHub. Download it from [Kaggle](https://www.kaggle.com/datasets/shivamb/fashion-clothing-products-catalog) and run the preprocessing scripts in order: `filter_data.py` → `prepare_text.py`.

---

## 📌 Key Engineering Decisions

| Decision | Reason |
|---|---|
| Filtered to 4 categories | Processing 1M+ rows was impractical; focused scope gives cleaner recommendations |
| Excluded `seller` from features | Including brand name biased results toward same-seller products |
| Deduplicated on `purl` | Some products had different IDs but identical URLs — genuine duplicates |
| On-demand cosine similarity | Pre-computing 86k×86k matrix would crash a standard laptop (60GB+ RAM) |
| TF-IDF over embeddings | Interpretable, fast, and appropriate for this scale without GPU |

---

## 👩‍💻 Author

**Khushi Sahu**
B.Tech CSE (AIML) · Manipal University Jaipur
[LinkedIn](https://www.linkedin.com/in/khushi-sahu-383760282/) · [GitHub](https://github.com/yourusername)
