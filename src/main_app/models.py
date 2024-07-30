from typing import Optional

from sqlmodel import SQLModel, Field

class Anime(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    synopsis: str
    poster_image: str

