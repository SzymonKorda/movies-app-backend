from rest_framework.utils.serializer_helpers import ReturnDict

from movies.models.movie import Movie
from movies.serializers.genre_serializer import FullGenreSerializer


class GenreService:
    def serialize_genres(self, movie: Movie) -> ReturnDict:
        return FullGenreSerializer(movie.genres.all(), many=True).data
