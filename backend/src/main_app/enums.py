from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"


class AnimeStatusEnum(str, Enum):
    CURRENT = "current"
    FINISHED = "finished"
    TBA = "tba"
    UPCOMING = "upcoming"
    UNRELEASED = "unreleased"


class AnimeShowTypeEnum(str, Enum):
    ONA = "ona"
    OVA = "ova"
    TV = "tv"
    MOVIE = "movie"
    MUSIC = "music"
    SPECIAL = "special"


class AnimeWatchingEnum(str, Enum):
    WATCHING = "watching"
    COMPLETED = "completed"
    DROPPED = "dropped"
    PLAN_TO_WATCH = "plan to watch"


class AnimeAgeRatingEnum(str, Enum):
    G = "G"
    PG = "PG"
    R = "R"
    R18 = "R18"
