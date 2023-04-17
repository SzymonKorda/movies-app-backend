import os
from datetime import datetime

from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser

from movies.models.actor import Actor
from movies.models.genre import GenreType
from movies.models.movie import Movie
from movies.serializers.movie import FullMovieSerializer, SimpleMovieSerializer
from movies.services.actor import ActorService
from movies.services.genre import GenreService
from movies.services.tmdb import TmdbService

tmdb_key = os.getenv('TMDB_KEY')
tmdb_uri = 'https://api.themoviedb.org/3'
headers = {'Authorization': 'Bearer ' + tmdb_key}


class MovieService:

    def __init__(self) -> None:
        self.actor_service = ActorService()
        self.tmdb_service = TmdbService()
        self.genre_service = GenreService()
        super().__init__()

    def get_movie(self, movie_id):
        try:
            movie = self.find_movie(movie_id)
        except Movie.DoesNotExist:
            return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
        movie_serializer = FullMovieSerializer(movie)
        return JsonResponse(movie_serializer.data, status=status.HTTP_200_OK)

    def get_all_movies(self):
        movies = Movie.objects.all()
        movies_serializer = SimpleMovieSerializer(movies, many=True)
        return JsonResponse(movies_serializer.data, safe=False)

    def create_movie(self, request):
        movie_id = JSONParser().parse(request)['movie_id']
        movie_details = self.tmdb_service.fetch_movie(movie_id)
        if not (movie_details.get('success', True)):
            return JsonResponse({'message': movie_details['status_message']}, status=status.HTTP_404_NOT_FOUND)

        trailer_path = self.prepare_trailer_path(movie_id)
        movie_credits = self.tmdb_service.fetch_movie_credits(movie_id)
        director = self.prepare_movie_director(movie_credits)

        movie = self.prepare_movie(director, movie_details, trailer_path)
        movie_serializer = FullMovieSerializer(data=movie)
        if movie_serializer.is_valid():
            movie = movie_serializer.save()
        else:
            if 'non_field_errors' in movie_serializer.errors:
                return JsonResponse({'message': movie_serializer.errors['non_field_errors']},
                                    status=status.HTTP_409_CONFLICT)
            else:
                return JsonResponse({'message': movie_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        self.prepare_movie_actors(movie, movie_credits)
        self.prepare_movie_genres(movie, movie_details)
        return JsonResponse(movie_serializer.data, status=status.HTTP_201_CREATED)

    def prepare_movie_genres(self, movie, movie_details):
        movie_genres = []
        if 'genres' in movie_details:
            for genre_details in movie_details['genres']:
                if genre_details['name'] in GenreType.values():
                    genre, created = self.genre_service.find_or_create_genre(genre_details)
                    movie_genres.append(genre)
        movie.genres.extend(movie_genres)

    def update_movie(self, movie_id, request):
        try:
            movie = self.find_movie(movie_id)
        except Movie.DoesNotExist:
            return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
        movie_data = JSONParser().parse(request)
        movie_serializer = FullMovieSerializer(movie, data=movie_data, partial=True)
        if movie_serializer.is_valid():
            movie_serializer.save()
            return JsonResponse(movie_serializer.data)
        return JsonResponse(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_movie(self, movie_id):
        try:
            movie = self.find_movie(movie_id)
        except Movie.DoesNotExist:
            return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return JsonResponse({'message': 'Movie was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    def get_movie_genres(self, movie_id):
        return self.find_movie_genres(movie_id)

    def get_movie_actors(self, movie_id):
        return self.find_movie_actors(movie_id)

    def find_movie(self, movie_id):
        return Movie.objects.get(pk=movie_id)

    def prepare_trailer_path(self, movie_id):
        movie_trailer = self.tmdb_service.fetch_movie_trailer(movie_id)
        official_trailers = list(filter(lambda trailer: trailer['official'], movie_trailer['results']))
        trailer_key = official_trailers[0]['key'] if official_trailers else movie_trailer['results'][0]['key']
        trailer_path = 'https://www.youtube.com/watch?v=' + trailer_key
        return trailer_path

    def prepare_movie(self, director, movie_details, trailer_path):
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

    def prepare_movie_director(self, movie_credits):
        return list(filter(lambda member: member['job'] == 'Director', movie_credits['crew']))[0]['name']

    def prepare_movie_actors(self, movie, movie_credits):
        movie_actors = self.actor_service.get_or_create_actors(movie_credits)
        movie.actors.extend(movie_actors)

    def find_movie_genres(self, movie_id):
        try:
            movie = self.find_movie(movie_id)
        except Movie.DoesNotExist:
            return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
        movie_genres = self.genre_service.serialize_genre(movie, True)
        return JsonResponse({'genres': movie_genres}, status=status.HTTP_200_OK)

    def find_movie_actors(self, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
        movie_actors = self.actor_service.serialize_to_simple_actor(movie, True)
        return JsonResponse({'actors': movie_actors.data}, status=status.HTTP_200_OK)

    def add_actor_to_movie(self, actor_id, movie_id):
        try:
            movie = self.find_movie(movie_id)
        except Movie.DoesNotExist:
            return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
        try:
            actor = self.actor_service.find_actor(actor_id)
        except Actor.DoesNotExist:
            return JsonResponse({'message': 'Actor does not exist'}, status=status.HTTP_404_NOT_FOUND)
        movie.actors.append(actor)
        return JsonResponse({'message': 'Actor added to movie successfully'}, status=status.HTTP_200_OK)
