from enum import Enum

from django.db import models


class GenreType(Enum):
    ACTION = 'Action'
    ADVENTURE = 'Adventure'
    ANIMATION = 'Animation'
    COMEDY = 'Comedy'
    CRIME = 'Crime'
    DOCUMENTARY = 'Documentary'
    DRAMA = 'Drama'
    FAMILY = 'Family'
    FANTASY = 'Fantasy'
    HISTORY = 'History'
    HORROR = 'Horror'
    MUSIC = 'Music'
    MYSTERY = 'Mystery'
    ROMANCE = 'Romance'
    SCIENCE_FICTION = 'Science Fiction'
    TV_MOVIE = 'TV Movie'
    THRILLER = 'Thriller'
    WAR = 'War'
    WESTERN = 'Western'

    @classmethod
    def values(cls):
        return set(map(lambda genre_type: genre_type.value, cls))


class Genre(models.Model):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "genre"
