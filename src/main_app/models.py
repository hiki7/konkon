from typing import Optional

from sqlmodel import SQLModel, Field


class AnimeCreate(SQLModel):
    title: str
    synopsis: str
    poster_image: str


class Anime(AnimeCreate, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # title: str
    # synopsis: str
    # poster_image: str

