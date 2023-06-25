from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "movies"

    def ready(self):
        from movies.serializers.genre_serializer import FullGenreSerializer
        from movies.services.tmdb_service import TmdbService

        genres: dict = TmdbService().fetch_genre_list()
        genre_serializer: FullGenreSerializer = FullGenreSerializer(
            data=genres["genres"], many=True
        )
        genre_serializer.is_valid()
        genre_serializer.save()
