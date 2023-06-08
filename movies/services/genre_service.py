from typing import Tuple, Union

from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from movies.models.genre import Genre
from movies.models.movie import Movie
from movies.serializers.genre_serializer import FullGenreSerializer
from movies.utils.genre_name import GenreName


class GenreService:
    def __init__(self) -> None:
        super().__init__()

    def find_or_create_genre(self, name: str) -> Union[Genre, None]:
        if name in GenreName.values():
            return Genre.objects.get_or_create(name=name)[0]
        return None

    def serialize_genres(self, movie: Movie) -> ReturnDict:
        return FullGenreSerializer(movie.genres.all(), many=True).data
