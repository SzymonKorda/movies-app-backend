from typing import Tuple

from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from movies.models.genre import Genre
from movies.models.movie import Movie
from movies.serializers.genre_serializer import FullGenreSerializer


class GenreService:
    def __init__(self) -> None:
        super().__init__()

    def find_or_create_genre(self, name: str) -> Tuple[Genre, bool]:
        return Genre.objects.get_or_create(name=name)

    def serialize_genres(self, movie: Movie) -> ReturnDict:
        return FullGenreSerializer(movie.genres.all(), many=True).data
