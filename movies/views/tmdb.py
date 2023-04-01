import json
import os
from datetime import datetime

import requests
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from movies.models import GenreType, Genre, Actor
from movies.serializers.actor import FullActorSerializer
from movies.serializers.genre import FullGenreSerializer
from movies.serializers.movie import FullMovieSerializer


class TmdbView(APIView):
    @staticmethod
    def get(request, movie_id):
        return create_movie(movie_id)


# return JsonResponse(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def load_genres():
    genres = [genre_type.value for genre_type in GenreType]
    for genre in genres:
        genre_serializer = FullGenreSerializer(data={
            'name': genre
        })
        if genre_serializer.is_valid():
            genre_serializer.save()


def create_movie(movie_id):
    tmdb_key = os.getenv('TMDB_KEY')
    tmdb_uri = 'https://api.themoviedb.org/3'
    headers = {'Authorization': 'Bearer ' + tmdb_key}


    movie_details_response = requests.get(tmdb_uri + '/movie/' + str(movie_id), headers=headers)
    movie_details = json.loads(movie_details_response.content)
    if not (movie_details.get('success', True)):
        return JsonResponse({'message': movie_details['status_message']}, status=status.HTTP_404_NOT_FOUND)
    movie_trailer_response = requests.get(tmdb_uri + '/movie/' + str(movie_id) + '/videos', headers=headers)
    movie_trailer = json.loads(movie_trailer_response.content)
    official_trailers = list(filter(lambda trailer: trailer['official'], movie_trailer['results']))
    trailer_key = official_trailers[0]['key'] if official_trailers else movie_trailer['results'][0]['key']
    trailer_path = 'https://www.youtube.com/watch?v=' + trailer_key
    movie_credits_response = requests.get(tmdb_uri + '/movie/' + str(movie_id) + '/credits', headers=headers)
    movie_credits = json.loads(movie_credits_response.content)
    director = list(filter(lambda member: member['job'] == 'Director', movie_credits['crew']))[0]['name']
    movie = prepare_movie(director, movie_details, trailer_path)
    actors_data = movie_credits['cast'][:5]
    movie_serializer = FullMovieSerializer(data=movie)
    if movie_serializer.is_valid():
        movie = movie_serializer.save()
    else:
        return JsonResponse({'message': movie_serializer.errors['non_field_errors']},
                            status=status.HTTP_409_CONFLICT)
    for details in actors_data:
        actor_details_response = requests.get(tmdb_uri + '/person/' + str(details['id']), headers=headers)
        actor_details = json.loads(actor_details_response.content)
        actor_data = prepare_actor(actor_details)
        actor_serializer = FullActorSerializer(data=actor_data)
        try:
            actor_serializer.is_valid(raise_exception=True)
            movie.actors.add(actor_serializer.save())
        except ValidationError as e:
            if e.detail['non_field_errors'][0].code == 'unique':
                existing_actor = Actor.objects.filter(
                    Q(name=actor_data['name']) & Q(date_of_birth=actor_data['date_of_birth'])).first()
                movie.actors.add(existing_actor)

    if bool(movie_details.get('genres')):
        for genre_details in movie_details['genres']:
            genre, created = Genre.objects.get_or_create(name=genre_details['name'])
            if genre:
                movie.genres.add(genre)
    return JsonResponse(movie_serializer.data, status=status.HTTP_201_CREATED)


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
