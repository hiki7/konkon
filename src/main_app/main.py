from fastapi import FastAPI, Request, Response, HTTPException
from pydantic import BaseModel
import requests
from typing import List, Optional
from .models import Anime
from .config.db_connect import engine

from sqlmodel import SQLModel, Session, create_engine, Field

app = FastAPI()

URL = "https://kitsu.io/api/edge/anime"
HEADERS = {
    "Accept": "application/vnd.api+json",
    "Content-Type": "application/vnd.api+json"
}


# class Anime(BaseModel):
#     anime_id: str
#     user_id: str

# class AnimeItemResponse(BaseModel):
#     id: str
#     title: str
#     synopsis: str
#     poster_image: str


# Fetch the list of anime
# @app.get("/anime", response_model=List[AnimeItemResponse])
# def fetch_anime():
#     response = requests.get(url, headers=headers)
#
#     if response.status_code == 200:
#         anime_list = response.json()['data']
#         return [
#             {
#                 "id": anime["id"],
#                 "title": anime["attributes"]["canonicalTitle"],
#                 "synopsis": anime["attributes"]["synopsis"],
#                 "poster_image": anime["attributes"]["posterImage"]["medium"],
#             }
#             for anime in anime_list
#         ]
#     else:
#         raise HTTPException(status_code=response.status_code, detail="Failed to fetch anime list")


@app.post("/save-anime")
def save_anime():
    response = requests.get(URL, headers=HEADERS)

    if response.status_code == 200:
        anime_list = response.json()['data']
        anime_objects = [
            Anime(
                title=anime['attributes']['canonicalTitle'],
                synopsis=anime['attributes']['synopsis'],
                poster_image=anime['attributes']['posterImage']['medium']
            )
            for anime in anime_list
        ]

        with Session(engine) as session:
            session.add_all(anime_objects)
            session.commit()
        return {"message": "Anime saved!"}
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to save anime!")

@app.get("/anime", response_model=List[Anime])
def get_anime():
    with Session(engine) as session:
        anime_list = session.query(Anime).all()
        return anime_list
