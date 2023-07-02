from datetime import datetime
from typing import Union, Any, List

from rest_framework import serializers

from movies.models.movie import Movie

TMDB_IMAGE_URI = "https://image.tmdb.org/t/p/w500"
IMDB_MOVIE_URI = "https://www.imdb.com/title/"


class FullMovieSerializer(serializers.ModelSerializer[Movie]):
    overview = serializers.CharField(source="description")
    budget = serializers.FloatField(source="box_office")
    runtime = serializers.IntegerField(source="duration")
    imdb_id = serializers.CharField(source="imdb_path")
    director = serializers.SerializerMethodField()
    trailer_path = serializers.SerializerMethodField()

    def to_representation(self, instance) -> Any:
        representation = super().to_representation(instance)
        representation["genres"] = self.initial_data["genre_names"]
        return representation

    class Meta:
        id = serializers.ReadOnlyField()
        model = Movie
        fields = (
            "id",
            "title",
            "overview",
            "budget",
            "runtime",
            "release_date",
            "poster_path",
            "backdrop_path",
            "adult",
            "imdb_id",
            "revenue",
            "status",
            "tagline",
            "director",
            "trailer_path",
        )

    def get_trailer_path(self, results):
        return self.prepare_trailer_path()

    def get_director(self, director):
        return self.prepare_movie_director()

    def get_box_office(self, budget):
        return float(budget)

    def get_release_date(self, release_date):
        return datetime.strptime(release_date, "%Y-%m-%d").date()

    def get_poster_path(self, poster_path):
        return self.prepare_resource_path(TMDB_IMAGE_URI, poster_path)

    def get_backdrop_path(self, backdrop_path):
        return self.prepare_resource_path(TMDB_IMAGE_URI, backdrop_path)

    def get_imdb_path(self, imdb_id):
        return self.prepare_resource_path(IMDB_MOVIE_URI, imdb_id)

    def get_revenue(self, revenue):
        return float(revenue)

    def prepare_movie_director(self):
        crew = self.initial_data["crew"]
        return next(member["name"] for member in crew if member["job"] == "Director")

    def prepare_trailer_path(self) -> str:
        movie_trailers = self.initial_data["results"]
        official_trailers: List[dict] = [
            trailer for trailer in movie_trailers if trailer["official"]
        ]
        trailer_key: str = (
            official_trailers[0]["key"]
            if official_trailers
            else movie_trailers[0]["key"]
        )
        return "https://www.youtube.com/watch?v=" + trailer_key

    @staticmethod
    def prepare_resource_path(
        resource_uri: str, resource_key: Union[str, None]
    ) -> Union[str, None]:
        return resource_uri + resource_key if resource_key else None


class SimpleMovieSerializer(serializers.ModelSerializer[Movie]):
    class Meta:
        id = serializers.ReadOnlyField()
        model = Movie
        fields = (
            "id",
            "title",
            "release_date",
            "duration",
            "description",
            "poster_path",
        )


class SearchMovieSerializer(serializers.ModelSerializer[Movie]):
    class Meta:
        id = serializers.ReadOnlyField()
        model = Movie
        fields = ("id", "title", "poster_path")
