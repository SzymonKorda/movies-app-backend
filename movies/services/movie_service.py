import os
from typing import List, Dict

from django.db import transaction
from rest_framework.exceptions import NotFound
from rest_framework.utils.serializer_helpers import ReturnDict

from movies.models import MovieGenre, Genre
from movies.models.actor import Actor
from movies.models.movie import Movie
from movies.payload.tmdb_movie_search_response import TmdbMovieSearchResponse
from movies.serializers.genre_serializer import FullGenreSerializer
from movies.serializers.movie_serializer import (
    FullTmdbMovieSerializer,
    SearchMovieSerializer,
    SimpleMovieSerializer,
    FullMovieSerializer,
)
from movies.services.actor_service import ActorService
from movies.services.genre_service import GenreService

tmdb_key = os.getenv("TMDB_KEY")
tmdb_uri = "https://api.themoviedb.org/3"
headers = {"Authorization": "Bearer " + tmdb_key} if tmdb_key else None


class MovieService:
    def __init__(self, tmdb_service) -> None:
        self.tmdb_service = tmdb_service
        self.actor_service = ActorService()
        self.genre_service = GenreService()

    def get_movie(self, movie_id: int) -> dict:
        return FullMovieSerializer(self.find_movie(movie_id)).data

    def get_all_movies(self) -> List[Dict]:
        return SimpleMovieSerializer(Movie.objects.all(), many=True).data

    @transaction.atomic
    def create_movie(self, movie_id: int) -> dict:
        movie_request = self.prepare_movie_data(movie_id)
        serializer = FullTmdbMovieSerializer(data=movie_request)
        serializer.is_valid(raise_exception=True)
        movie: Movie = serializer.save()
        # TODO: return id directly from serializer .data
        return {"id": movie.id, **serializer.validated_data}

    def add_genres_to_movie(self, tmdb_movie_id):
        movie_data = self.tmdb_service.fetch_movie(tmdb_movie_id)
        movie_id = Movie.objects.filter(title=movie_data["title"]).get().id
        genre_names = [genre["name"] for genre in movie_data["genres"]]
        genres = self.genre_service.get_genres_by_name(genre_names)
        movie_genres = [
            MovieGenre(movie_id=movie_id, genre_id=genre["id"]) for genre in genres
        ]
        MovieGenre.objects.bulk_create(movie_genres)

    def get_genres_from_movie(self, movie_id):
        movie_genres = list(MovieGenre.objects.filter(movie_id=movie_id).all().values())
        genres_id = [movie_genre["genre_id"] for movie_genre in movie_genres]
        return FullGenreSerializer(
            Genre.objects.filter(id__in=genres_id), many=True
        ).data

    def prepare_movie_data(self, movie_id: int) -> dict:
        movie_details: dict = self.tmdb_service.fetch_movie(movie_id)
        movie_trailer: dict = self.tmdb_service.fetch_movie_trailer(movie_id)
        movie_credits: dict = self.tmdb_service.fetch_movie_credits(movie_id)
        return {**movie_details, **movie_credits, **movie_trailer}

    def update_movie(self, movie_id: int, update_request: dict) -> ReturnDict:
        movie: Movie = self.find_movie(movie_id)
        movie_serializer: FullMovieSerializer = FullMovieSerializer(
            movie, data=update_request, partial=True
        )
        movie_serializer.is_valid(raise_exception=True)
        movie_serializer.save()
        return movie_serializer.data

    def delete_movie(self, movie_id) -> None:
        movie: Movie = self.find_movie(movie_id)
        movie.delete()

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
