from datetime import datetime
from typing import Union

from rest_framework import serializers
from rest_framework.fields import DictField

from movies.models import Actor
from movies.models.movie import Movie

TMDB_IMAGE_URI = "https://image.tmdb.org/t/p/w500"
IMDB_MOVIE_URI = "https://www.imdb.com/title/"

class CrewSerializer(serializers.Serializer):
    name = serializers.CharField()

    def get_name(self, crew):
        print(crew)

class FullMovieSerializer(serializers.ModelSerializer[Movie]):
    overview = serializers.CharField(source="description")
    budget = serializers.FloatField(source="box_office")
    runtime = serializers.IntegerField(source="duration")
    imdb_id = serializers.CharField(source="imdb_path")
    # crew = serializers.ListSerializer(source="director", child)

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
            # "crew",
        )

    def get_crew(self, crew):
        return next(member.name for member in crew if member.job == "Director")

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
