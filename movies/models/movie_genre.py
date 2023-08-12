from django.db import models

from movies.models import Movie, Genre


# TODO: django does not support composite primary keys
class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        db_table = "movie_genre"
        unique_together = ("movie_id", "genre_id")
