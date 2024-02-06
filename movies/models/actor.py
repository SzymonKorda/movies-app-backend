from datetime import date, datetime
from typing import Union

from django.db import models

from movies.payload.tmdb_actor_response import TmdbActorResponse

IMDB_MOVIE_URI = "https://www.imdb.com/title/"


class Actor(models.Model):
    name = models.CharField(max_length=50, default="")
    biography = models.CharField(max_length=5000, default="")
    place_of_birth = models.CharField(max_length=50, default="")
    date_of_birth = models.DateField(default=date.today)
    imdb_path = models.CharField(max_length=50, default="")
    poster_path = models.CharField(max_length=500, default="")

    class Meta:
        db_table = "actor"
        unique_together = ("name", "date_of_birth")

    @classmethod
    def from_response(cls, actor_details: dict):
        name: str = actor_details["name"]
        biography: str = actor_details["biography"]
        place_of_birth: Union[str, None] = actor_details["place_of_birth"]
        birthday: Union[str, None] = actor_details["birthday"]
        date_of_birth: Union[date, None] = (
            datetime.strptime(birthday, "%Y-%m-%d").date() if birthday else None
        )
        imdb_path: str = actor_details["imdb_id"]
        poster_path: Union[str, None] = cls.prepare_resource_path(
            IMDB_MOVIE_URI, actor_details["profile_path"]
        )
        return cls(
            name=name,
            biography=biography,
            place_of_birth=place_of_birth,
            date_of_birth=date_of_birth,
            imdb_path=imdb_path,
            poster_path=poster_path,
        )

    @staticmethod
    def prepare_resource_path(
        resource_uri: str, resource_key: Union[str, None]
    ) -> Union[str, None]:
        return resource_uri + resource_key if resource_key else None
