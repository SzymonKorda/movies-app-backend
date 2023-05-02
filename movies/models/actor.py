from datetime import date, datetime

from django.db import models, IntegrityError
from rest_framework.exceptions import ValidationError

from movies.payload.tmdb_actor_response import TmdbActorResponse


class ActorManager(models.Manager['Actor']):
    def create_actor(self, actor_details: TmdbActorResponse):
        name: str = actor_details.name
        biography: str = actor_details.biography
        place_of_birth: str = actor_details.place_of_birth
        date_of_birth: date = datetime.strptime(actor_details.birthday, '%Y-%m-%d').date()
        imdb_id: str = actor_details.imdb_id
        poster_path: str = self.prepare_poster_path(actor_details.profile_path)
        try:
            actor: Actor = self.create(name=name, biography=biography, place_of_birth=place_of_birth,
                                       date_of_birth=date_of_birth, imdb_id=imdb_id, poster_path=poster_path)
        except IntegrityError:
            raise ValidationError(
                detail=f'Actor with given name and date of birth ({name}, {date_of_birth}) already exists')
        return actor

    def prepare_poster_path(self, resource_key: str):
        return 'https://image.tmdb.org/t/p/w500' + resource_key if resource_key else None


class Actor(models.Model):
    name = models.CharField(max_length=50, default='')
    biography = models.CharField(max_length=5000, default='')
    place_of_birth = models.CharField(max_length=50, default='')
    date_of_birth = models.DateField(default=date.today)
    imdb_id = models.CharField(max_length=50, default='')
    poster_path = models.CharField(max_length=500, default='')

    objects = ActorManager()

    class Meta:
        db_table = "actor"
        unique_together = ('name', 'date_of_birth')
