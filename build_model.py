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

    # Combine features
    df["combined"] = df.apply(
        lambda x: f"{x['genre']} {x['genre']} {x['language']} {x['description']}",
        axis=1
    )

    # TF-IDF
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(df["combined"])

    print("TF-IDF matrix shape:", matrix.shape)

    # ✅ SAVE MATRIX (NOT similarity)
    with open("model/similarity.pkl", "wb") as f:
        pickle.dump((matrix, df), f)

    print("✅ Model built and saved!")


if __name__ == "__main__":
    build_model()