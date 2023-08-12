from movies.models import Genre, MovieGenre
from movies.serializers.genre_serializer import FullGenreSerializer


class GenreService:
    def get_genres_by_name(self, movie_genres):
        return list(Genre.objects.filter(name__in=movie_genres).all().values())

    def get_genres_from_movie(self, movie_id):
        movie_genres = list(MovieGenre.objects.filter(movie_id=movie_id).all().values())
        genres_id = [movie_genre['genre_id'] for movie_genre in movie_genres]
        return FullGenreSerializer(Genre.objects.filter(id__in=genres_id), many=True).data

