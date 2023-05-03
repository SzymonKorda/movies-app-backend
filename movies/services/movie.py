import os
from typing import List, Union, Mapping

from django.db.models import QuerySet
from django.forms.models import model_to_dict
from django.http import HttpRequest
from rest_framework.exceptions import NotFound, ValidationError, ErrorDetail
from rest_framework.parsers import JSONParser
from rest_framework.utils.serializer_helpers import ReturnDict

from movies.models.actor import Actor
from movies.models.genre import Genre
from movies.models.movie import Movie
from movies.payload.movie_update_request import MovieUpdateRequest
from movies.payload.tmdb_movie_credits_response import TmdbMovieCreditsResponse
from movies.payload.tmdb_movie_crew_member_response import TmdbMovieCrewMemberResponse
from movies.payload.tmdb_movie_response import TmdbMovieResponse
from movies.payload.tmdb_movie_search_response import TmdbMovieSearchResponse
from movies.payload.tmdb_movie_trailer_response import TmdbMovieTrailerResponse
from movies.serializers.movie import FullMovieSerializer, SearchMovieSerializer
from movies.services.actor import ActorService
from movies.services.genre import GenreService
from movies.services.tmdb import TmdbService

tmdb_key = os.getenv('TMDB_KEY')
tmdb_uri = 'https://api.themoviedb.org/3'
headers = {'Authorization': 'Bearer ' + tmdb_key} if tmdb_key else None


class MovieService:

    def __init__(self) -> None:
        self.actor_service = ActorService()
        self.tmdb_service = TmdbService()
        self.genre_service = GenreService()
        super().__init__()

    def get_movie(self, movie_id: int) -> Movie:
        return self.find_movie(movie_id)

    def get_all_movies(self, search_query: str) -> List[Movie]:
        movies: QuerySet[Movie] = Movie.objects.filter(title__icontains=search_query)
        return list(movies)

    def create_movie(self, request: HttpRequest) -> ReturnDict:
        movie_id: int = JSONParser().parse(request)['movie_id']
        movie_details: TmdbMovieResponse = self.tmdb_service.fetch_movie(movie_id)
        trailer_path: str = self.prepare_trailer_path(movie_id)
        movie_credits: TmdbMovieCreditsResponse = self.tmdb_service.fetch_movie_credits(movie_id)
        director: str = self.prepare_movie_director(movie_credits.crew_members)
        movie: Movie = Movie.from_response(movie_details, trailer_path, director)
        movie_serializer = FullMovieSerializer(data=model_to_dict(movie))
        try:
            movie_serializer.is_valid(raise_exception=True)
        except ValidationError as ex:
            non_field_errors_key: Union[ErrorDetail, None] = ex.args[0]['non_field_errors'][0] \
                if 'non_field_errors' in ex.args[0] else None
            if non_field_errors_key and non_field_errors_key.code == 'unique':
                raise ValidationError(
                    detail=f'Movie with given title and release date ({movie.title}, {movie.release_date}) already exists'
                )
            else:
                raise ex

        movie = movie_serializer.save()
        self.prepare_movie_actors(movie, movie_credits.cast_members)
        self.prepare_movie_genres(movie, movie_details.genres)
        return movie_serializer.data

    def prepare_movie_genres(self, movie: Movie, genres: List[str]) -> None:
        movie_genres: List[Genre] = []
        for name in genres:
            genre: Genre = self.genre_service.find_or_create_genre(name)[0]
            movie_genres.append(genre)
        movie.genres.add(*movie_genres)

    def update_movie(self, movie_id: int, request: HttpRequest) -> ReturnDict:
        movie: Movie = self.find_movie(movie_id)
        movie_data: Mapping[str, MovieUpdateRequest] = JSONParser().parse(request)
        movie_serializer: FullMovieSerializer = FullMovieSerializer(movie, data=movie_data, partial=True)
        movie_serializer.is_valid(raise_exception=True)
        movie_serializer.save()
        return movie_serializer.data

    def delete_movie(self, movie_id) -> None:
        movie: Movie = self.find_movie(movie_id)
        movie.delete()

    def get_movie_genres(self, movie_id: int) -> ReturnDict:
        movie: Movie = self.find_movie(movie_id)
        return self.genre_service.serialize_genres(movie)

    def get_movie_actors(self, movie_id: int) -> ReturnDict:
        movie: Movie = self.find_movie(movie_id)
        return self.actor_service.serialize_to_simple_actors(movie)

    def find_movie(self, movie_id: int) -> Movie:
        try:
            movie: Movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            raise NotFound(detail={'detail': f'Movie with id {movie_id} does not exist'})
        return movie

    def prepare_trailer_path(self, movie_id: int) -> str:
        movie_trailers: List[TmdbMovieTrailerResponse] = self.tmdb_service.fetch_movie_trailer(movie_id)
        official_trailers: List[TmdbMovieTrailerResponse] = [trailer for trailer in movie_trailers if trailer.official]
        trailer_key: str = official_trailers[0].key if official_trailers else movie_trailers[0].key
        return 'https://www.youtube.com/watch?v=' + trailer_key

    def prepare_movie_director(self, crew_members: List[TmdbMovieCrewMemberResponse]) -> str:
        return next(member.name for member in crew_members if member.job == 'Director')

    def prepare_movie_actors(self, movie: Movie, cast_members: List[int]) -> None:
        movie_actors: List[Actor] = self.actor_service.get_or_create_actors(cast_members)
        movie.actors.add(*movie_actors)

    def add_actor_to_movie(self, actor_id: int, movie_id: int) -> None:
        movie: Movie = self.find_movie(movie_id)
        actor: Actor = self.actor_service.find_actor(actor_id)
        movie.actors.add(actor)

    def movie_admin_search(self, search_query: str) -> ReturnDict:
        search_results: List[TmdbMovieSearchResponse] = self.tmdb_service.movie_search(search_query)
        movie_serializer: SearchMovieSerializer = SearchMovieSerializer(data=search_results, many=True)
        movie_serializer.is_valid()
        return movie_serializer.data
