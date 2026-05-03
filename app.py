from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
import importlib
import model.recommender as rec_module
from model.recommender import recommend_for_user
from build_model import build_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up — rebuilding recommendation model...")
    try:
        build_model()
        importlib.reload(rec_module)
        print(" Model built successfully on startup")
    except Exception as e:
        print(f"Model build failed on startup: {e} — using existing pkl if available")
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5000",
        "https://regional-ottbackfinal-1.onrender.com",  
        "https://regional-ott.vercel.app",              
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserInput(BaseModel):
    user_likes: list[str]


@app.post("/recommend")
def recommend(data: UserInput):
    recommendations = recommend_for_user(data.user_likes, top_n=4)
    return {"recommendations": recommendations}


@app.post("/rebuild")
def rebuild():
    try:
        build_model()
        importlib.reload(rec_module)
        return {"status": " Model rebuilt successfully"}
    except Exception as e:
        return {"status": f" Rebuild failed: {str(e)}"}


@app.get("/health")
def health():
    return {"status": "ok"}


# python -m uvicorn app:app --reload --port 8000