from movies.models import Genre


class GenreService:
    def get_genres_by_name(self, movie_genres):
        return list(Genre.objects.filter(name__in=movie_genres).all().values())

