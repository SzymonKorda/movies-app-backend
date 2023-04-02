from datetime import datetime
import json
import os

import requests
from django.db import connection
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from movies.models.actor import Actor
from movies.models.movie import Movie
from movies.serializers.actor import SimpleActorSerializer, FullActorSerializer
from movies.serializers.movie import SimpleMovieSerializer

tmdb_key = os.getenv('TMDB_KEY')
tmdb_uri = 'https://api.themoviedb.org/3'
headers = {'Authorization': 'Bearer ' + tmdb_key}


class ActorView(APIView):

    @staticmethod
    def get(request, actor_id=None):
        if actor_id:
            return get_actor(actor_id)
        return get_all_actors()

    @staticmethod
    def post(request):
        return create_actor(request)

    @staticmethod
    def put(request, actor_id):
        return update_actor(actor_id, request)

    @staticmethod
    def delete(request, actor_id):
        return delete_actor(actor_id)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]


class ActorMoviesView(APIView):
    # permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, movie_id, actor_id):
        return add_movie_to_actor(actor_id, movie_id)

    @staticmethod
    def get(request, actor_id):
        return get_movies_from_actor(actor_id)


def get_movies_from_actor(actor_id):
    try:
        actor = Actor.objects.get(pk=actor_id)
    except Actor.DoesNotExist:
        return JsonResponse({'message': 'Actor does not exist'}, status=status.HTTP_404_NOT_FOUND)
    movie_serializer = SimpleMovieSerializer(actor.movie_set.all(), many=True)
    return JsonResponse({'movies': movie_serializer.data}, status=status.HTTP_200_OK)


def add_movie_to_actor(actor_id, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
    try:
        actor = Actor.objects.get(pk=actor_id)
    except Actor.DoesNotExist:
        return JsonResponse({'message': 'Actor does not exist'}, status=status.HTTP_404_NOT_FOUND)
    movie.actors.add(actor)
    return JsonResponse({'message': 'Actor added to movie successfully'}, status=status.HTTP_200_OK)


def delete_actor(actor_id):
    try:
        actor = Actor.objects.get(pk=actor_id)
    except Actor.DoesNotExist:
        return JsonResponse({'message': 'Actor does not exist'}, status=status.HTTP_404_NOT_FOUND)

    actor.delete()
    return JsonResponse({'message': 'Actor was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


def update_actor(actor_id, request):
    try:
        actor = Actor.objects.get(pk=actor_id)
    except Actor.DoesNotExist:
        return JsonResponse({'message': 'Actor does not exist'}, status=status.HTTP_404_NOT_FOUND)
    actor_data = JSONParser().parse(request)
    actor_serializer = FullActorSerializer(actor, data=actor_data, partial=True)
    if actor_serializer.is_valid():
        actor_serializer.save()
        return JsonResponse(actor_serializer.data)
    return JsonResponse(actor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_all_actors():
    actors = Actor.objects.all()
    actor_serializer = SimpleActorSerializer(actors, many=True)
    return JsonResponse(actor_serializer.data, safe=False)


def get_actor(actor_id):
    try:
        actor = Actor.objects.get(pk=actor_id)
    except Actor.DoesNotExist:
        return JsonResponse({'message': 'Actor does not exist'}, status=status.HTTP_404_NOT_FOUND)
    actor_serializer = FullActorSerializer(actor)
    return JsonResponse(actor_serializer.data, status=status.HTTP_200_OK)


def fetch_actor_movies(actor_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT movie_id FROM movie_actors WHERE actor_id = %s", [actor_id])
        rows = cursor.fetchall()
    return rows


def create_actor(request):
    actor_id = JSONParser().parse(request)['actor_id']
    actor_details = fetch_actor(actor_id, headers, tmdb_uri)
    actor = prepare_actor(actor_details)
    actor_serializer = FullActorSerializer(data=actor)
    if actor_serializer.is_valid():
        actor_serializer.save()
        return JsonResponse(actor_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(actor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def fetch_actor(actor_id, headers, tmdb_uri):
    actor_details_response = requests.get(tmdb_uri + '/person/' + str(actor_id), headers=headers)
    actor_details = json.loads(actor_details_response.content)
    return actor_details


def prepare_actor(actor_details):
    return {
        'name': actor_details['name'],
        'biography': actor_details['biography'],
        'place_of_birth': actor_details['place_of_birth'],
        'date_of_birth': datetime.strptime(actor_details['birthday'], '%Y-%m-%d').date(),
        'imdb_id': actor_details['imdb_id'],
        'poster_path': 'https://image.tmdb.org/t/p/w500' + actor_details['profile_path']
    }
