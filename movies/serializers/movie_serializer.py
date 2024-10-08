from datetime import datetime
from typing import List, Any

from rest_framework import serializers

from movies.models.movie import Movie


class FullTmdbMovieSerializer(serializers.ModelSerializer[Movie]):
    overview = serializers.CharField(source="description")
    budget = serializers.FloatField(source="box_office")
    runtime = serializers.IntegerField(source="duration")
    imdb_id = serializers.CharField(source="imdb_key")
    director = serializers.SerializerMethodField()
    trailer_key = serializers.SerializerMethodField()
    poster_path = serializers.CharField(source="poster_key")
    backdrop_path = serializers.CharField(source="backdrop_key")
    id = serializers.IntegerField(source="tmdb_id")

    # TODO: find a better way to return SerializerMethodField fields
    #  or another way to add custom logic for serializer field (e.g: director)
    def validate(self, attrs: Any) -> Any:
        attrs.update({"director": self.prepare_movie_director()})
        attrs.update({"trailer_key": self.prepare_trailer_key()})
        return super().validate(attrs)

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
            "trailer_key",
        )

    def get_trailer_key(self, trailer_key):
        return self.prepare_trailer_key()

    def get_director(self, director):
        return self.prepare_movie_director()

    def get_box_office(self, budget):
        return float(budget)

    def get_release_date(self, release_date):
        return datetime.strptime(release_date, "%Y-%m-%d").date()

    def get_revenue(self, revenue):
        return float(revenue)

    def prepare_movie_director(self):
        crew = self.initial_data["crew"]
        return next(member["name"] for member in crew if member["job"] == "Director")

    def prepare_trailer_key(self) -> str:
        movie_trailers = self.initial_data["results"]
        official_trailers: List[dict] = [
            trailer for trailer in movie_trailers if trailer["official"]
        ]
        trailer_key: str = (
            official_trailers[0]["key"]
            if official_trailers
            else movie_trailers[0]["key"]
        )
        return trailer_key


class FullMovieSerializer(serializers.ModelSerializer[Movie]):
    class Meta:
        id = serializers.ReadOnlyField()
        model = Movie
        fields = "__all__"


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
            "poster_key",
        )


class SearchMovieSerializer(serializers.ModelSerializer[Movie]):
    class Meta:
        id = serializers.ReadOnlyField()
        model = Movie
        fields = ("id", "title", "poster_path")
