import os
from datetime import datetime
from typing import List

from django.db.models import QuerySet
from django.http import JsonResponse, HttpRequest
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import JSONParser

from movies.models.actor import Actor
from movies.models.genre import GenreType
from movies.models.movie import Movie
from movies.payload.tmdb_movie_credits_response import TmdbMovieCreditsResponse
from movies.payload.tmdb_movie_crew_member_response import TmdbMovieCrewMemberResponse
from movies.payload.tmdb_movie_response import TmdbMovieResponse
from movies.payload.tmdb_movie_trailer_response import TmdbMovieTrailerResponse
from movies.serializers.movie import FullMovieSerializer, SearchMovieSerializer
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

    def get_movie(self, movie_id: int) -> Movie:
        try:
            movie: Movie = self.find_movie(movie_id)
        except Movie.DoesNotExist as ex:
            raise NotFound(detail={'detail': f'Movie with id {movie_id} does not exist'})
        return movie

    def get_all_movies(self, search_query: str) -> List[Movie]:
        movies: QuerySet[Movie] = Movie.objects.filter(title__icontains=search_query)
        return list(movies)

    def create_movie(self, request: HttpRequest):
        movie_id: int = JSONParser().parse(request)['movie_id']
        movie_details: TmdbMovieResponse = self.tmdb_service.fetch_movie(movie_id)
        trailer_path: str = self.prepare_trailer_path(movie_id)
        movie_credits: TmdbMovieCreditsResponse = self.tmdb_service.fetch_movie_credits(movie_id)
        director: str = self.prepare_movie_director(movie_credits.crew_members)
        movie = Movie.objects.create_movie(movie_details, trailer_path, director)
        # movie_serializer = FullMovieSerializer(data=movie)
        # if movie_serializer.is_valid(raise_exception=True):
        #     movie: Movie = movie_serializer.save()
        # self.prepare_movie_actors(movie, movie_credits.cast_members)
        # self.prepare_movie_genres(movie, movie_details)
        # return JsonResponse(movie_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse({'hehe': 'hehe'}, status=status.HTTP_201_CREATED)

    def prepare_movie_genres(self, movie, movie_details):
        movie_genres = []
        if 'genres' in movie_details:
            for genre_details in movie_details['genres']:
                if genre_details['name'] in GenreType.values():
                    genre, created = self.genre_service.find_or_create_genre(genre_details)
                    movie_genres.append(genre)
        [movie.genres.add(genre.id) for genre in movie_genres]

    def update_movie(self, movie_id: int, request: HttpRequest):
        try:
            movie: Movie = self.find_movie(movie_id)
        except Movie.DoesNotExist:
            return None
        movie_data: dict = JSONParser().parse(request)
        movie_serializer: FullMovieSerializer = FullMovieSerializer(movie, data=movie_data, partial=True)
        if movie_serializer.is_valid():
            movie_serializer.save()
            return Movie(movie_serializer.data)
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

    def find_movie(self, movie_id: int) -> Movie:
        return Movie.objects.get(pk=movie_id)

    def prepare_trailer_path(self, movie_id: int) -> str:
        movie_trailers: List[TmdbMovieTrailerResponse] = self.tmdb_service.fetch_movie_trailer(movie_id)
        official_trailers: List[TmdbMovieTrailerResponse] = [trailer for trailer in movie_trailers if trailer.official]
        trailer_key: str = official_trailers[0].key if official_trailers else movie_trailers[0].key
        return 'https://www.youtube.com/watch?v=' + trailer_key

    def prepare_movie_director(self, crew_members: List[TmdbMovieCrewMemberResponse]) -> str:
        return next(member.name for member in crew_members if member.job == 'Director')

    def prepare_movie_actors(self, movie: Movie, cast_members: List[int]):
        movie_actors = self.actor_service.get_or_create_actors(cast_members)
        [movie.actors.add(actor.id) for actor in movie_actors]

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
        return JsonResponse({'actors': movie_actors}, status=status.HTTP_200_OK)

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

    def movie_admin_search(self, search_query):
        search_results = self.tmdb_service.movie_search(search_query)
        results = [self.preapre_search_movie(result) for result in search_results]
        return JsonResponse({'results': results}, status=status.HTTP_200_OK)

    def preapre_search_movie(self, result):
        movie = SearchMovieSerializer(data={
            'title': result['title'],
            'poster_path': 'https://image.tmdb.org/t/p/w500' + str(result['poster_path'])
        })
        movie.is_valid()
        return dict(movie.data, id=result['id'])

