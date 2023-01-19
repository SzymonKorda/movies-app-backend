from django.db import models


class Actor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    born_place = models.CharField(max_length=50)
    born_year = models.IntegerField()
    height = models.IntegerField()

    class Meta:
        db_table = "actor"


class Movie(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    box_office = models.FloatField()
    duration = models.IntegerField()
    release_year = models.IntegerField()
    actors = models.ManyToManyField(Actor, blank=True)

    class Meta:
        db_table = "movie"

    def __str__(self):
        return self.title
