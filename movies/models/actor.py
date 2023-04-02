import datetime

from django.db import models


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
