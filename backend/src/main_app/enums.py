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
