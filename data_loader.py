import requests

API_URL = "http://localhost:5000/api/video/movies"

def fetch_movies():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()

        json_data = response.json()
        movies = json_data.get("data", [])

        # 🔥 DEBUG PRINT
        print("Total movies fetched:", len(movies))
        print("First movie:", movies[0] if movies else "No data")

        return movies

    except Exception as e:
        print("Error fetching data:", e)
        return []
    

if __name__ == "__main__":
    print("Running data loader...")   # 👈 ADD THIS
    fetch_movies()