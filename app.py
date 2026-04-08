from fastapi import FastAPI
from pydantic import BaseModel
from model.recommender import recommend_for_user

app = FastAPI()

class UserInput(BaseModel):
    user_likes: list[str]

@app.post("/recommend")
def recommend(data: UserInput):
    recommendations = recommend_for_user(data.user_likes, top_n=4)
    return {"recommendations": recommendations}


# Uvicorn running on http://127.0.0.1:8000