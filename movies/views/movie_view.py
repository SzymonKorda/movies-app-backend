from typing import Optional

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import APIView

from movies.models.movie import Movie
from movies.serializers.movie_serializer import (
    FullTmdbMovieSerializer,
    SimpleMovieSerializer,
    FullMovieSerializer,
)
from movies.services.genre_service import GenreService
from movies.services.movie_service import MovieService
from movies.services.tmdb_service import TmdbService


# TODO: ask about ReturnList, ReturnDict and serialized types (serializer.data)
class MovieView(APIView):
    movie_service: MovieService = MovieService(TmdbService())

    def get(self, request: HttpRequest, movie_id: Optional[int] = None) -> JsonResponse:
        if movie_id:
            movie: Movie = self.movie_service.get_movie(movie_id)
            return JsonResponse({"data": movie}, status=status.HTTP_200_OK)
        movies = self.movie_service.get_all_movies()
        return JsonResponse({"data": movies}, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest) -> JsonResponse:
        movie_id: int = JSONParser().parse(request)["movie_id"]
        movie: dict = self.movie_service.create_movie(movie_id)
        return JsonResponse({"data": movie}, status=status.HTTP_201_CREATED)

    def put(self, request: HttpRequest, movie_id: int) -> JsonResponse:
        movie: ReturnDict = self.movie_service.update_movie(movie_id, request)
        return JsonResponse({"data": movie}, status=status.HTTP_200_OK)

    def delete(self, request: HttpRequest, movie_id: int) -> JsonResponse:
        self.movie_service.delete_movie(movie_id)
        return JsonResponse(
            {"message": "Movie was deleted successfully!"}, status=status.HTTP_200_OK
        )

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]


class MovieActorsView(APIView):
    def __init__(self, *args, **kwargs):
        self.movie_service = MovieService(TmdbService())
        super().__init__(*args, **kwargs)

    # permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, movie_id: int) -> JsonResponse:
        movie_actors: ReturnDict = self.movie_service.get_movie_actors(movie_id)
        return JsonResponse({"data": movie_actors}, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest, movie_id: int, actor_id: int) -> JsonResponse:
        self.movie_service.add_actor_to_movie(actor_id, movie_id)
        return JsonResponse(
            {"message": "Actor added to movie successfully"}, status=status.HTTP_200_OK
        )


class MovieGenresView(APIView):
    def __init__(self, *args, **kwargs):
        self.movie_service = MovieService(TmdbService())
        self.genre_service = GenreService()
        super().__init__(*args, **kwargs)

    # permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest, movie_id: int):
        self.movie_service.add_genres_to_movie(movie_id)
        return JsonResponse(
            {"message": "Genres added to movie successfully"}, status=status.HTTP_200_OK
        )

    def get(self, request: HttpRequest, movie_id: int) -> JsonResponse:
        movie_genres = self.genre_service.get_genres_from_movie(movie_id)
        return JsonResponse({"data": movie_genres}, status=status.HTTP_200_OK)


class MovieSearchView(APIView):
    movie_service = MovieService(TmdbService())

    def get(self, request: HttpRequest) -> JsonResponse:
        search_query: str = request.GET.get("query", default="")
        movies: ReturnDict = self.movie_service.movie_admin_search(search_query)
        return JsonResponse({"data": movies}, status=status.HTTP_200_OK)
