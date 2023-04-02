import json
import os
from datetime import datetime

import requests
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from movies.models.actor import Actor
from movies.models.genre import GenreType, Genre
from movies.models.movie import Movie
from movies.serializers.actor import FullActorSerializer, SimpleActorSerializer
from movies.serializers.genre import FullGenreSerializer
from movies.serializers.movie import FullMovieSerializer, SimpleMovieSerializer

tmdb_key = os.getenv('TMDB_KEY')
tmdb_uri = 'https://api.themoviedb.org/3'
headers = {'Authorization': 'Bearer ' + tmdb_key}


class MovieView(APIView):

    @staticmethod
    def get(request, movie_id=None):
        if movie_id:
            return get_movie(movie_id)
        return get_all_movies()

    @staticmethod
    @transaction.atomic
    def post(request):
        return create_movie(request)

    @staticmethod
    def put(request, movie_id):
        return update_movie(movie_id, request)

    @staticmethod
    def delete(request, movie_id):
        return delete_movie(movie_id)

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]


class MovieActorsView(APIView):
    # permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, movie_id, actor_id):
        return add_actor_to_movie(actor_id, movie_id)

    @staticmethod
    def get(request, movie_id):
        return get_actors_from_movie(movie_id)


class MovieGenresView(APIView):
    # permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, movie_id):
        return get_genres_from_movie(movie_id)


def get_genres_from_movie(movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
    movie_serializer = FullGenreSerializer(movie.genres.all(), many=True)
    return JsonResponse({'genres': movie_serializer.data}, status=status.HTTP_200_OK)


def get_actors_from_movie(movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
    actor_serializer = SimpleActorSerializer(movie.actors.all(), many=True)
    return JsonResponse({'actors': actor_serializer.data}, status=status.HTTP_200_OK)


def add_actor_to_movie(actor_id, movie_id):
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


def update_movie(movie_id, request):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
    movie_data = JSONParser().parse(request)
    movie_serializer = FullMovieSerializer(movie, data=movie_data, partial=True)
    if movie_serializer.is_valid():
        movie_serializer.save()
        return JsonResponse(movie_serializer.data)
    return JsonResponse(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_movie(movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
    movie.delete()
    return JsonResponse({'message': 'Movie was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


def get_all_movies():
    movies = Movie.objects.all()
    movies_serializer = SimpleMovieSerializer(movies, many=True)
    return JsonResponse(movies_serializer.data, safe=False)


def get_movie(movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
    movie_serializer = FullMovieSerializer(movie)
    return JsonResponse(movie_serializer.data, status=status.HTTP_200_OK)


def create_movie(request):
    movie_id = JSONParser().parse(request)['movie_id']
    movie_details = fetch_movie(headers, movie_id, tmdb_uri)
    if not (movie_details.get('success', True)):
        return JsonResponse({'message': movie_details['status_message']}, status=status.HTTP_404_NOT_FOUND)

    trailer_path = prepare_trailer_path(headers, movie_id, tmdb_uri)
    movie_credits = fetch_movie_credits(headers, movie_id, tmdb_uri)
    director = prepare_movie_director(movie_credits)

    movie = prepare_movie(director, movie_details, trailer_path)
    movie_serializer = FullMovieSerializer(data=movie)
    if movie_serializer.is_valid():
        movie = movie_serializer.save()
    else:
        if 'non_field_errors' in movie_serializer.errors:
            return JsonResponse({'message': movie_serializer.errors['non_field_errors']},
                                status=status.HTTP_409_CONFLICT)
        else:
            return JsonResponse({'message': movie_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    prepare_movie_actors(headers, movie, movie_credits, tmdb_uri)
    prepare_movie_genres(movie, movie_details)
    return JsonResponse(movie_serializer.data, status=status.HTTP_201_CREATED)


def prepare_movie_genres(movie, movie_details):
    if 'genres' in movie_details:
        for genre_details in movie_details['genres']:
            if genre_details['name'] in GenreType.values():
                genre, created = Genre.objects.get_or_create(name=genre_details['name'])
                movie.genres.add(genre)


def prepare_movie_actors(headers, movie, movie_credits, tmdb_uri):
    actors = movie_credits['cast'][:5]
    for actor_data in actors:
        actor_details = fetch_actor(actor_data['id'], headers, tmdb_uri)
        actor = prepare_actor(actor_details)
        actor_serializer = FullActorSerializer(data=actor)
        try:
            actor_serializer.is_valid(raise_exception=True)
            movie.actors.add(actor_serializer.save())
        except ValidationError as ex:
            if ex.detail['non_field_errors'][0].code == 'unique':
                existing_actor = Actor.objects.filter(
                    Q(name=actor['name']) & Q(date_of_birth=actor['date_of_birth'])).first()
                movie.actors.add(existing_actor)


def fetch_actor(actor_id, headers, tmdb_uri):
    actor_details_response = requests.get(tmdb_uri + '/person/' + str(actor_id), headers=headers)
    actor_details = json.loads(actor_details_response.content)
    return actor_details


def prepare_movie_director(movie_credits):
    return list(filter(lambda member: member['job'] == 'Director', movie_credits['crew']))[0]['name']


def fetch_movie_credits(headers, movie_id, tmdb_uri):
    movie_credits_response = requests.get(tmdb_uri + '/movie/' + str(movie_id) + '/credits', headers=headers)
    return json.loads(movie_credits_response.content)


def fetch_movie(headers, movie_id, tmdb_uri):
    movie_details_response = requests.get(tmdb_uri + '/movie/' + str(movie_id), headers=headers)
    return json.loads(movie_details_response.content)


def prepare_trailer_path(headers, movie_id, tmdb_uri):
    movie_trailer = fetch_movie_trailer(headers, movie_id, tmdb_uri)
    official_trailers = list(filter(lambda trailer: trailer['official'], movie_trailer['results']))
    trailer_key = official_trailers[0]['key'] if official_trailers else movie_trailer['results'][0]['key']
    trailer_path = 'https://www.youtube.com/watch?v=' + trailer_key
    return trailer_path


def fetch_movie_trailer(headers, movie_id, tmdb_uri):
    movie_trailer_response = requests.get(tmdb_uri + '/movie/' + str(movie_id) + '/videos', headers=headers)
    movie_trailer = json.loads(movie_trailer_response.content)
    return movie_trailer


def prepare_actor(actor_details):
    return {
        'name': actor_details['name'],
        'biography': actor_details['biography'],
        'place_of_birth': actor_details['place_of_birth'],
        'date_of_birth': datetime.strptime(actor_details['birthday'], '%Y-%m-%d').date(),
        'imdb_id': actor_details['imdb_id'],
        'poster_path': 'https://image.tmdb.org/t/p/w500' + actor_details['profile_path']
    }


def prepare_movie(director, movie_details, trailer_path):
    return {
        'title': movie_details['original_title'],
        'description': movie_details['overview'],
        'box_office': movie_details['budget'],
        'duration': movie_details['runtime'],
        'release_date': datetime.strptime(movie_details['release_date'], '%Y-%m-%d').date(),
        'poster_path': 'https://image.tmdb.org/t/p/w500' + movie_details['poster_path'],
        'backdrop_path': 'https://image.tmdb.org/t/p/w500' + movie_details['backdrop_path'],
        'adult': movie_details['adult'],
        'imdb_path': 'https://www.imdb.com/title/' + movie_details['imdb_id'],
        'revenue': movie_details['revenue'],
        'status': movie_details['status'],
        'tagline': movie_details['tagline'],
        'trailer_path': trailer_path,
        'director': director,
    }
