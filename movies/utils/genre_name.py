import enum
from typing import List


# TODO: find way to create Django/PostgreSQL EnumField
class GenreName(enum.Enum):
    ACTION = "Action"
    ADVENTURE = "Adventure"
    ANIMATION = "Animation"
    COMEDY = "Comedy"
    CRIME = "Crime"
    DOCUMENTARY = "Documentary"
    DRAMA = "Drama"
    FAMILY = "Family"
    FANTASY = "Fantasy"
    HISTORY = "History"
    HORROR = "Horror"
    MUSIC = "Music"
    MYSTERY = "Mystery"
    ROMANCE = "Romance"
    SCIENCE_FICTION = "Science Fiction"
    TV_MOVIE = "TV Movie"
    THRILLER = "Thriller"
    WAR = "War"
    WESTERN = "Western"
    OTHER = "Other"

    @classmethod
    def values(cls) -> List[str]:
        return [name.value for name in GenreName]
