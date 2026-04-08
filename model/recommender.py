import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity

# Load model
with open("model/similarity.pkl", "rb") as f:
    vectors, df = pickle.load(f)


def recommend_for_user(user_likes, top_n=4):

    indices = []

    # Step 1: find movie indices
    for movie in user_likes:
        try:
            idx = df[df['title'].str.lower() == movie.lower()].index[0]
            indices.append(idx)
        except:
            print(f"Movie not found: {movie}")

    if len(indices) == 0:
        return ["No valid movies found"]

    # Step 2: create user profile vector
    user_vector = np.mean(vectors[indices].toarray(), axis=0)

    # Step 3: compute similarity
    similarity = cosine_similarity([user_vector], vectors.toarray())[0]

    # Step 4: sort
    movies_list = sorted(
        list(enumerate(similarity)),
        key=lambda x: x[1],
        reverse=True
    )

    # Step 5: recommend
    recommendations = []

    for i in movies_list:
        title = df.iloc[i[0]]["title"]

        if title not in user_likes:
            recommendations.append(title)

        if len(recommendations) == top_n:
            break

    return recommendations


# 🔥 Test
if __name__ == "__main__":
    print(recommend_for_user(["Himalayan Revenge Begin", "The Last Journey"]))