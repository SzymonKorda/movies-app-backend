from datetime import date

from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=500, default="", blank=True)
    box_office = models.FloatField(default=0.0)
    duration = models.IntegerField(default=0, blank=True)
    release_date = models.DateField(default=date.today)
    poster_key = models.CharField(max_length=500, default="")
    backdrop_key = models.CharField(max_length=500, default="")
    adult = models.BooleanField(default=True)
    imdb_key = models.CharField(max_length=50, default="", blank=True)
    revenue = models.FloatField(default=0.0)
    status = models.CharField(max_length=50, default="")
    tagline = models.CharField(max_length=500, default="", blank=True)
    trailer_key = models.CharField(max_length=500, default="")
    director = models.CharField(max_length=50, default="")

    class Meta:
        db_table = "movie"
        unique_together = ("title", "release_date")

    def __str__(self):
        return self.title
