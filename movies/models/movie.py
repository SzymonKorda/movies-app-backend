from datetime import date, datetime
from typing import Union

from django.db import models

from movies.payload.tmdb_movie_response import TmdbMovieResponse


class Movie(models.Model):
    title = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=500, default="", blank=True)
    box_office = models.FloatField(default=0.0)
    duration = models.IntegerField(default=0, blank=True)
    release_date = models.DateField(default=date.today)
    poster_path = models.CharField(max_length=500, default="")
    backdrop_path = models.CharField(max_length=500, default="")
    adult = models.BooleanField(default=True)
    imdb_path = models.CharField(max_length=50, default="", blank=True)
    revenue = models.FloatField(default=0.0)
    status = models.CharField(max_length=50, default="")
    tagline = models.CharField(max_length=500, default="", blank=True)
    trailer_path = models.CharField(max_length=500, default="")
    director = models.CharField(max_length=50, default="")
    genres = models.ManyToManyField("Genre", blank=True)
    actors = models.ManyToManyField("Actor", blank=True)

    # @classmethod
    # def from_response(
    #     cls, movie_details: TmdbMovieResponse, trailer_path: str, director: str
    # ):
    #     title: str = movie_details.original_title
    #     description: str = movie_details.overview
    #     box_office: float = float(movie_details.budget)
    #     duration: Union[int, None] = movie_details.runtime
    #     release_date: date = datetime.strptime(
    #         movie_details.release_date, "%Y-%m-%d"
    #     ).date()
    #     poster_path: Union[str, None] = cls.prepare_resource_path(
    #         TMDB_IMAGE_URI, movie_details.poster_path
    #     )
    #     backdrop_path: Union[str, None] = cls.prepare_resource_path(
    #         TMDB_IMAGE_URI, movie_details.backdrop_path
    #     )
    #     adult: bool = movie_details.adult
    #     imdb_path: Union[str, None] = cls.prepare_resource_path(
    #         IMDB_MOVIE_URI, movie_details.imdb_id
    #     )
    #     revenue: float = float(movie_details.revenue)
    #     status: str = movie_details.status
    #     tagline: Union[str, None] = movie_details.tagline
    #     return cls(
    #         title=title,
    #         description=description,
    #         box_office=box_office,
    #         duration=duration,
    #         release_date=release_date,
    #         poster_path=poster_path,
    #         backdrop_path=backdrop_path,
    #         adult=adult,
    #         imdb_path=imdb_path,
    #         revenue=revenue,
    #         status=status,
    #         tagline=tagline,
    #         trailer_path=trailer_path,
    #         director=director,
    #     )

    class Meta:
        db_table = "movie"
        unique_together = ("title", "release_date")

    def __str__(self):
        return self.title
