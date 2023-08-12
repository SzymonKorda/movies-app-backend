from typing import List

from movies.models import Genre
from movies.models.movie import Movie
from movies.serializers.genre_serializer import FullGenreSerializer


class GenreService:
    def serialize_genres(self, movie: Movie) -> List[Genre]:
        return FullGenreSerializer(movie.genres.all(), many=True).data

    def get_genres_by_name(self, movie_genres):
        # genre_serializer = FullGenreSerializer(data=movie_genres, many=True)
        # genre_serializer.is_valid(raise_exception=True)

        return list(Genre.objects.filter(name__in=movie_genres).all().values())
