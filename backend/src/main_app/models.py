from typing import Optional, List, Dict
from sqlmodel import SQLModel, Field, Relationship
from .enums import RoleEnum, AnimeStatusEnum, AnimeShowTypeEnum, AnimeWatchingEnum


class UserAnime(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    anime_id: int = Field(foreign_key="anime.id")
    watch_status: AnimeWatchingEnum

    user: "User" = Relationship(back_populates="anime_list")
    anime: "Anime" = Relationship(back_populates="user_anime_list")


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
    user_anime_list: List[UserAnime] = Relationship(back_populates="anime")


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
    anime_list: List[UserAnime] = Relationship(back_populates="user")


