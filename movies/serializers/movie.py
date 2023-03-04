from rest_framework import serializers

from movies.models import Movie


class FullMovieSerializer(serializers.ModelSerializer):
    class Meta:
        id = serializers.ReadOnlyField()
        model = Movie
        fields = '__all__'


class SimpleMovieSerializer(serializers.ModelSerializer):
    class Meta:
        id = serializers.ReadOnlyField()
        model = Movie
        fields = ('id', 'title', 'release_year', 'duration', 'description', 'image')
