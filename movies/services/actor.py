from datetime import datetime

from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser

from movies.models.actor import Actor
from movies.models.movie import Movie
from movies.serializers.actor import FullActorSerializer, SimpleActorSerializer
from movies.serializers.movie import SimpleMovieSerializer
from movies.services.tmdb import TmdbService


class ActorService:

    def __init__(self) -> None:
        self.tmdb_service = TmdbService()
        super().__init__()

    def get_actor(self, actor_id):
        try:
            actor = self.find_actor(actor_id)
        except Actor.DoesNotExist:
            return JsonResponse({'message': 'Actor does not exist'}, status=status.HTTP_404_NOT_FOUND)
        actor_serializer = FullActorSerializer(actor)
        return JsonResponse(actor_serializer.data, status=status.HTTP_200_OK)

    def get_all_actors(self):
        actors = Actor.objects.all()
        actor_serializer = SimpleActorSerializer(actors, many=True)
        return JsonResponse(actor_serializer.data, safe=False)

    def create_actor(self, request):
        actor_id = JSONParser().parse(request)['actor_id']
        actor_details = self.tmdb_service.fetch_actor(actor_id)
        actor = self.prepare_actor(actor_details)
        actor_serializer = FullActorSerializer(data=actor)
        if actor_serializer.is_valid():
            actor_serializer.save()
            return JsonResponse(actor_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(actor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_actor(self, actor_id, request):
        try:
            actor = self.find_actor(actor_id)
        except Actor.DoesNotExist:
            return JsonResponse({'message': 'Actor does not exist'}, status=status.HTTP_404_NOT_FOUND)
        actor_data = JSONParser().parse(request)
        actor_serializer = FullActorSerializer(actor, data=actor_data, partial=True)
        if actor_serializer.is_valid():
            actor_serializer.save()
            return JsonResponse(actor_serializer.data)
        return JsonResponse(actor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_actor(self, actor_id):
        try:
            actor = self.find_actor(actor_id)
        except Actor.DoesNotExist:
            return JsonResponse({'message': 'Actor does not exist'}, status=status.HTTP_404_NOT_FOUND)
        actor.delete()
        return JsonResponse({'message': 'Actor was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    def get_movies_from_actor(self, actor_id):
        try:
            actor = Actor.objects.get(pk=actor_id)
        except Actor.DoesNotExist:
            return JsonResponse({'message': 'Actor does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serialized_movies = SimpleMovieSerializer(actor.movie_set.all(), many=True).data
        return JsonResponse({'movies': serialized_movies}, status=status.HTTP_200_OK)

    def add_movie_to_actor(self, actor_id, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
        try:
            actor = Actor.objects.get(pk=actor_id)
        except Actor.DoesNotExist:
            return JsonResponse({'message': 'Actor does not exist'}, status=status.HTTP_404_NOT_FOUND)
        actor.movie_set.add(movie)
        return JsonResponse({'message': 'Actor added to movie successfully'}, status=status.HTTP_200_OK)

    def prepare_actor(self, actor_details):
        return {
            'name': actor_details['name'],
            'biography': actor_details['biography'],
            'place_of_birth': actor_details['place_of_birth'],
            'date_of_birth': datetime.strptime(actor_details['birthday'], '%Y-%m-%d').date(),
            'imdb_id': actor_details['imdb_id'],
            'poster_path': 'https://image.tmdb.org/t/p/w500' + actor_details['profile_path']
        }

    def find_actor(self, actor_id):
        return Actor.objects.get(pk=actor_id)

    def get_or_create_actors(self, movie_credits):
        actors = movie_credits['cast'][:5]
        movie_actors = []
        for actor_data in actors:
            actor_details = self.tmdb_service.fetch_actor(actor_data['id'])
            actor = self.prepare_actor(actor_details)
            actor_serializer = FullActorSerializer(data=actor)
            try:
                actor_serializer.is_valid(raise_exception=True)
                movie_actors.append(actor_serializer.save())
            except ValidationError as ex:
                if ex.detail['non_field_errors'][0].code == 'unique':
                    existing_actor = Actor.objects.filter(
                        Q(name=actor['name']) & Q(date_of_birth=actor['date_of_birth'])).first()
                    movie_actors.append(existing_actor)
        return movie_actors

    def find_movie_actors(self, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
        actor_serializer = SimpleActorSerializer(movie.actors.all(), many=True)
        return JsonResponse({'actors': actor_serializer.data}, status=status.HTTP_200_OK)

    def serialize_to_simple_actor(self, movie, many):
        return SimpleActorSerializer(movie.actors.all(), many=many).data
