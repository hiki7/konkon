from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional
from .models import *
from .enums import RoleEnum, AnimeWatchingEnum
from .config.db_connect import engine
from sqlmodel import SQLModel, Session, select
from passlib.context import CryptContext

import requests

app = FastAPI()

URL = "https://kitsu.io/api/edge/anime"
HEADERS = {
    "Accept": "application/vnd.api+json",
    "Content-Type": "application/vnd.api+json"
}

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


# JWT Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency functions
def get_user(username: str):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
        return user

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user.password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_admin_user(current_user: User = Depends(get_current_active_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

# Routes
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/create-users", response_model=User)
def create_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_data = User(username=user.username, email=user.email, password=hashed_password, role=user.role)
    with Session(engine) as session:
        session.add(user_data)
        session.commit()
        session.refresh(user_data)
        return user_data



@app.post("/save-anime")
def save_anime():
    response = requests.get(URL, headers=HEADERS)

    if response.status_code == 200:
        anime_list = response.json()['data']
        anime_objects = []

        with Session(engine) as session:
            for anime in anime_list:
                anime_categories = []
                categories_response = requests.get(anime['relationships']['categories']['links']['related'], headers=HEADERS)
                if categories_response.status_code == 200:
                    categories_data = categories_response.json()['data']
                    for category in categories_data:
                        category_obj = session.exec(select(Category).where(Category.id == int(category['id']))).first()
                        if not category_obj:
                            category_obj = Category(
                                id=int(category['id']),
                                title=category['attributes']['title'],
                                description=category['attributes']['description']
                            )
                            session.add(category_obj)
                        anime_categories.append(category_obj)

                anime_obj = Anime(
                    title=anime['attributes']['canonicalTitle'],
                    synopsis=anime['attributes']['synopsis'],
                    poster_image=anime['attributes']['posterImage']['medium'],
                    start_date=anime['attributes']['startDate'],
                    end_date=anime['attributes']['endDate'],
                    status=anime['attributes']['status'],
                    episode_count=anime['attributes']['episodeCount'],
                    show_type=anime['attributes']['showType'],
                    age_rating=anime['attributes']['ageRating'],
                    age_rating_guide=anime['attributes']['ageRatingGuide'],
                    categories=anime_categories
                )
                anime_objects.append(anime_obj)

            session.add_all(anime_objects)
            session.commit()

        return {"message": "Anime and categories saved!"}
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to save anime!")

@app.get("/anime", response_model=List[AnimeListResponse])
def get_anime(
        category_title: Optional[str] = None,
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1)
):
    with Session(engine) as session:
        query = select(Anime)
        if category_title:
            query = query.join(Anime.categories).where(Category.title == category_title)

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size).order_by(Anime.id.desc())

        anime_list = session.exec(query).all()
        return anime_list


@app.get("/anime/{anime_id}", response_model=AnimeDetailResponse)
def get_anime_detail(anime_id: int):
    with Session(engine) as session:
        anime = session.get(Anime, anime_id)
        if not anime:
            raise HTTPException(status_code=404, detail="Anime not found")

        anime_detail = AnimeDetailResponse(
            id=anime.id,
            title=anime.title,
            synopsis=anime.synopsis,
            poster_image=anime.poster_image,
            start_date=anime.start_date,
            end_date=anime.end_date,
            status=anime.status,
            episode_count=anime.episode_count,
            show_type=anime.show_type,
            age_rating=anime.age_rating,
            age_rating_guide=anime.age_rating_guide,
            categories=[CategoryResponse(id=cat.id, title=cat.title, description=cat.description) for cat in anime.categories]
        )

        return anime_detail


@app.post("/add-anime", response_model=Anime, dependencies=[Depends(get_admin_user)])
def create_anime(anime: AnimeCreate):
    with Session(engine) as session:
        db_anime = Anime.from_orm(anime)
        session.add(db_anime)
        session.commit()
        session.refresh(db_anime)
        return db_anime


@app.patch("/anime/{anime_id}", response_model=Anime, dependencies=[Depends(get_admin_user)])
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


@app.delete("/anime/{anime_id}", response_model=Anime, dependencies=[Depends(get_admin_user)])
def delete_anime(anime_id: int):
    with Session(engine) as session:
        db_anime = session.get(Anime, anime_id)
        session.delete(db_anime)
        session.commit()
        return db_anime


@app.post("/user/anime", response_model=UserAnime)
async def add_anime_to_user_list(
    anime_id: int,
    status: AnimeWatchingEnum,
    current_user: User = Depends(get_current_user)
):
    if status is None:
        raise HTTPException(status_code=400, detail="Watch status must be provided.")
    user_anime = UserAnime(user_id=current_user.id, anime_id=anime_id, watch_status=status)
    with Session(engine) as session:
        session.add(user_anime)
        session.commit()
        session.refresh(user_anime)
        return user_anime


@app.get("/user/anime", response_model=List[UserAnime])
async def get_user_anime_list(
        current_user: User = Depends(get_current_user),
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1)
):
    with Session(engine) as session:
        query = select(UserAnime).where(UserAnime.user_id == current_user.id)

        offset = (page - 1) * page_size
        user_anime_list = session.exec(query.offset(offset).limit(page_size)).all()

        return user_anime_list


@app.patch("/user/anime/{user_anime_id}", response_model=UserAnime)
async def update_user_anime_status(user_anime_id: int, status: AnimeWatchingEnum, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        user_anime = session.get(UserAnime, user_anime_id)
        if not user_anime or user_anime.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Anime not found in your list!")
        user_anime.watch_status = status
        session.add(user_anime)
        session.commit()
        session.refresh(user_anime)
        return user_anime


@app.delete("/user/anime/{user_anime_id}", response_model=UserAnime)
async def delete_anime_from_user_list(user_anime_id: int, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        user_anime = session.get(UserAnime, user_anime_id)
        if not user_anime or user_anime.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Anime not found in your list!")
        session.delete(user_anime)
        session.commit()
        return user_anime
