import datetime

from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=500, default='')
    box_office = models.FloatField(default=0.0)
    duration = models.IntegerField(default=0)
    release_date = models.DateField(default=datetime.date.today)
    poster_path = models.CharField(max_length=500, default='')
    backdrop_path = models.CharField(max_length=500, default='')
    adult = models.BooleanField(default=True)
    imdb_path = models.CharField(max_length=50, default='')
    revenue = models.FloatField(default=0.0)
    status = models.CharField(max_length=50, default='')
    tagline = models.CharField(max_length=500, default='')
    trailer_path = models.CharField(max_length=500, default='')
    director = models.CharField(max_length=50, default='')

    genres = models.ManyToManyField('Genre', blank=True)
    actors = models.ManyToManyField('Actor', blank=True)

    class Meta:
        db_table = "movie"
        unique_together = ('title', 'release_date')

    def __str__(self):
        return self.title


class Actor(models.Model):
    name = models.CharField(max_length=50, default='')
    biography = models.CharField(max_length=5000, default='')
    place_of_birth = models.CharField(max_length=50, default='')
    date_of_birth = models.DateField(default=datetime.date.today)
    imdb_id = models.CharField(max_length=50, default='')
    poster_path = models.CharField(max_length=500, default='')

    class Meta:
        db_table = "actor"
        unique_together = ('name', 'date_of_birth')


class Genre(models.Model):
    name = models.CharField(max_length=50, default='', unique=True)

    class Meta:
        db_table = "genre"

