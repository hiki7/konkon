from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date
from .enums import RoleEnum, AnimeStatusEnum, AnimeShowTypeEnum


class AnimeCreate(SQLModel):
    title: str
    synopsis: str
    poster_image: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: AnimeStatusEnum
    episode_count: Optional[int] = None
    show_type: AnimeShowTypeEnum


class Anime(AnimeCreate, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class AnimeUpdate(SQLModel):
    title: Optional[str] = None
    synopsis: Optional[str] = None
    poster_image: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[AnimeStatusEnum] = None
    episode_count: Optional[int] = None
    show_type: Optional[AnimeShowTypeEnum] = None


class UserCreate(SQLModel):
    username: str
    email: str
    password: str
    role: RoleEnum


class User(UserCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

