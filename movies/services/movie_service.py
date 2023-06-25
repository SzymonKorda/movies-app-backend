import os
from typing import List, Mapping

from django.db.models import QuerySet
from django.http import HttpRequest
from rest_framework.exceptions import NotFound
from rest_framework.parsers import JSONParser
from rest_framework.utils.serializer_helpers import ReturnDict

from movies.models.actor import Actor
from movies.models.genre import Genre
from movies.models.movie import Movie
from movies.payload.movie_update_request import MovieUpdateRequest
from movies.payload.tmdb_movie_search_response import TmdbMovieSearchResponse
from movies.serializers.movie_serializer import (
    FullMovieSerializer,
    SearchMovieSerializer,
)
from movies.services.actor_service import ActorService
from movies.services.genre_service import GenreService
from movies.utils.genre_name import GenreName

tmdb_key = os.getenv("TMDB_KEY")
tmdb_uri = "https://api.themoviedb.org/3"
headers = {"Authorization": "Bearer " + tmdb_key} if tmdb_key else None


class MovieService:
    def __init__(self, tmdb_service) -> None:
        self.tmdb_service = tmdb_service
        self.actor_service = ActorService()
        self.genre_service = GenreService()
        self.serializer = FullMovieSerializer()

    def get_movie(self, movie_id: int) -> Movie:
        return self.find_movie(movie_id)

    def get_all_movies(self, search_query: str) -> QuerySet[Movie]:
        return Movie.objects.filter(title__icontains=search_query)

    def create_movie(self, movie_id: int) -> ReturnDict:
        movie_details: dict = self.tmdb_service.fetch_movie(movie_id)
        movie_trailer: dict = self.tmdb_service.fetch_movie_trailer(movie_id)
        movie_credits: dict = self.tmdb_service.fetch_movie_credits(movie_id)
        director: str = self.prepare_movie_director(movie_credits["crew"])
        trailer: str = self.prepare_trailer_path(movie_trailer["results"])
        movie_request = {**movie_details, **{"director": director}, **{"trailer_path": trailer}}
        movie_serializer = FullMovieSerializer(data=movie_request)
        movie_serializer.is_valid(raise_exception=True)
        movie: Movie = movie_serializer.save()
        # self.prepare_movie_genres(movie, movie_details.genres)
        return movie_serializer.data

    # def create_movie_with_actors_and_genres(self, movie_id: int) -> ReturnDict:
    #     movie_details: TmdbMovieResponse = self.tmdb_service.fetch_movie(movie_id)
    #     trailer_path: str = self.prepare_trailer_path(movie_id)
    #     movie_credits: TmdbMovieCreditsResponse = self.tmdb_service.fetch_movie_credits(
    #         movie_id
    #     )
    #     director: str = self.prepare_movie_director(movie_credits.crew_members)
    #     movie: Movie = Movie.from_response(movie_details, trailer_path, director)
    #     movie_serializer = FullMovieSerializer(data=model_to_dict(movie))
    #     movie_serializer.is_valid(raise_exception=True)
    #     movie = movie_serializer.save()
    #     self.prepare_movie_actors(movie, movie_credits.cast_members)
    #     self.prepare_movie_genres(movie, movie_details.genres)
    #     return movie_serializer.data

    def prepare_movie_genres(self, movie: Movie, genres: List[str]) -> None:
        movie_genres: List[Genre] = []
        for name in genres:
            # get all żanra = ()

            genre = GenreName(name)

            # if name in GenreName.values():
            #     genre: Genre = self.genre_service.find_or_create_genre(name)
            movie_genres.append(genre)
        movie.genres.add(*movie_genres)

        movie = genres.select(genre=lala)

    def update_movie(self, movie_id: int, request: HttpRequest) -> ReturnDict:
        movie: Movie = self.find_movie(movie_id)
        movie_data: Mapping[str, MovieUpdateRequest] = JSONParser().parse(request)
        movie_serializer: FullMovieSerializer = FullMovieSerializer(
            movie, data=movie_data, partial=True
        )
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
            raise NotFound(
                detail={"detail": f"Movie with id {movie_id} does not exist"}
            )
        return movie

    def prepare_trailer_path(self, movie_trailers: dict) -> str:
        official_trailers: List[dict] = [
            trailer for trailer in movie_trailers if trailer["official"]
        ]
        trailer_key: str = (
            official_trailers[0]["key"]
            if official_trailers
            else movie_trailers[0]["key"]
        )
        return "https://www.youtube.com/watch?v=" + trailer_key

    def prepare_movie_director(self, crew_members: dict) -> str:
        return next(
            member["name"] for member in crew_members if member["job"] == "Director"
        )

    def prepare_movie_actors(self, movie: Movie, cast_members: List[int]) -> None:
        movie_actors: List[Actor] = self.actor_service.get_or_create_actors(
            cast_members
        )
        movie.actors.add(*movie_actors)

    def add_actor_to_movie(self, actor_id: int, movie_id: int) -> None:
        movie: Movie = self.find_movie(movie_id)
        actor: Actor = self.actor_service.find_actor(actor_id)
        movie.actors.add(actor)

    def movie_admin_search(self, search_query: str) -> ReturnDict:
        search_results: List[TmdbMovieSearchResponse] = self.tmdb_service.movie_search(
            search_query
        )
        movie_serializer: SearchMovieSerializer = SearchMovieSerializer(
            data=search_results, many=True
        )
        movie_serializer.is_valid()
        return movie_serializer.data
