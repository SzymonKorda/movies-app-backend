from rest_framework import serializers

from movies.models.movie import Movie


class FullMovieSerializer(serializers.ModelSerializer[Movie]):
    class Meta:
        id = serializers.ReadOnlyField()
        model = Movie
        fields = (
            'id', 'title', 'description', 'box_office', 'duration', 'release_date', 'poster_path', 'backdrop_path',
            'adult', 'imdb_path', 'revenue', 'status', 'tagline', 'trailer_path', 'director')


class SimpleMovieSerializer(serializers.ModelSerializer[Movie]):
    class Meta:
        id = serializers.ReadOnlyField()
        model = Movie
        fields = ('id', 'title', 'release_date', 'duration', 'description', 'poster_path')


class SearchMovieSerializer(serializers.ModelSerializer[Movie]):
    class Meta:
        id = serializers.ReadOnlyField()
        model = Movie
        fields = ('id', 'title', 'poster_path')
