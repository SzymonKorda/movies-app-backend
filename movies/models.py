from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    box_office = models.FloatField()
    duration = models.IntegerField()
    release_year = models.IntegerField()
    image = models.CharField(max_length=500, default='')
    actors = models.ManyToManyField('Actor', blank=True, related_name="movies")

    class Meta:
        db_table = "movie"

    def __str__(self):
        return self.title


class Actor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    born_place = models.CharField(max_length=50)
    born_year = models.IntegerField()
    height = models.IntegerField()
    image = models.CharField(max_length=500, default='')

    class Meta:
        db_table = "actor"
