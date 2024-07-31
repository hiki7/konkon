from fastapi import FastAPI, Request, Response, HTTPException
from pydantic import BaseModel
import requests
from typing import List, Optional
from .models import Anime, AnimeCreate, AnimeUpdate
from .config.db_connect import engine

from sqlmodel import SQLModel, Session, create_engine, Field, select

app = FastAPI()

URL = "https://kitsu.io/api/edge/anime"
HEADERS = {
    "Accept": "application/vnd.api+json",
    "Content-Type": "application/vnd.api+json"
}


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
        anime_list = session.exec(select(Anime)).all()
        return anime_list


@app.post("/create-anime", response_model=Anime)
def create_anime(anime: AnimeCreate):
    with Session(engine) as session:
        db_anime = Anime.from_orm(anime)
        session.add(db_anime)
        session.commit()
        session.refresh(db_anime)
        return db_anime


@app.patch("/anime/{anime_id}", response_model=Anime)
def update_anime(anime_id: int, anime: AnimeUpdate):
    with Session(engine) as session:
        db_anime = session.get(Anime, anime_id)
    if not db_anime:
        raise HTTPException(status_code=404, detail="Anime not found!")
    anime_data = anime.dict(exclude_unset=True)
    for key, value in anime_data.items():
        setattr(db_anime, key, value)
    session.add(db_anime)
    session.commit()
    session.refresh(db_anime)
    return db_anime


@app.delete("/anime/{anime_id}", response_model=Anime)
def delete_anime(anime_id: int):
    with Session(engine) as session:
        db_anime = session.get(Anime, anime_id)
        session.delete(db_anime)
        session.commit()
        return db_anime
