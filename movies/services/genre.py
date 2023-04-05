from django.http import JsonResponse
from rest_framework import status

from movies.models.genre import Genre, GenreType
from movies.models.movie import Movie
from movies.serializers.genre import FullGenreSerializer
from movies.services.movie import MovieService


class GenreService:

    def __init__(self) -> None:
        self.movie_service = MovieService()
        super().__init__()

    def find_or_create_genre(self, genre_details):
        return Genre.objects.get_or_create(name=genre_details['name'])

    def serialize_genre(self, movie, many):
        return FullGenreSerializer(movie.genres.all(), many=many).data
