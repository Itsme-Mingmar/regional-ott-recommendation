import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from data_loader import fetch_movies
import pickle

def build_model():
    print("Fetching movies...")
    movies = fetch_movies()

    if not movies:
        print("No data found!")
        return

    print("Total movies:", len(movies))

    # Convert to DataFrame
    df = pd.DataFrame(movies)

    # Optional safe drop
    df = df.drop(columns=["_id"], errors="ignore")

    # ✅ Fill missing fields so TF-IDF doesn't crash
    df["genre"] = df["genre"].fillna("")
    df["description"] = df["description"].fillna("")
    df["language"] = df["language"].fillna("")

    # ✅ Convert genre array to string if needed
    df["genre_str"] = df["genre"].apply(
        lambda x: " ".join(x) if isinstance(x, list) else str(x)
    )

    # ✅ Print all movies going into model so you can verify
    print("Movies in model:", df["title"].tolist())

    # Combine features — genre weighted 3x for better matching
    df["combined"] = df.apply(
        lambda x: f"{x['genre_str']} {x['genre_str']} {x['genre_str']} {x['language']} {x['description']}",
        axis=1
    )

    # TF-IDF
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(df["combined"])

    print("TF-IDF matrix shape:", matrix.shape)

    # SAVE MATRIX
    with open("model/similarity.pkl", "wb") as f:
        pickle.dump((matrix, df), f)

    print("✅ Model built and saved!")


if __name__ == "__main__":
    build_model()