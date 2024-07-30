from fastapi import FastAPI, Request, Response, HTTPException
from pydantic import BaseModel
import requests
from typing import List
from models import AnimeItem
from config.db_connect import engine

app = FastAPI()

url = "https://kitsu.io/api/edge/anime"
headers = {
    "Accept": "application/vnd.api+json",
    "Content-Type": "application/vnd.api+json"
}


# class Anime(BaseModel):
#     anime_id: str
#     user_id: str

class AnimeItemResponse(BaseModel):
    id: str
    title: str
    synopsis: str
    poster_image: str


# Fetch the list of anime
@app.get("/anime", response_model=List[AnimeItemResponse])
def fetch_anime():
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        anime_list = response.json()['data']
        return [
            {
                "id": anime["id"],
                "title": anime["attributes"]["canonicalTitle"],
                "synopsis": anime["attributes"]["synopsis"],
                "poster_image": anime["attributes"]["posterImage"]["medium"],
            }
            for anime in anime_list
        ]
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch anime list")
