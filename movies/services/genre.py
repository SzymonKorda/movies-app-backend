from typing import Tuple

from movies.models.genre import Genre
from movies.serializers.genre import FullGenreSerializer


class GenreService:

    def __init__(self) -> None:
        super().__init__()

    def find_or_create_genre(self, name: str) -> Tuple[Genre, bool]:
        return Genre.objects.get_or_create(name=name)

    def serialize_genre(self, movie, many):
        return FullGenreSerializer(movie.genres.all(), many=many).data
