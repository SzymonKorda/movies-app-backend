from rest_framework import serializers

from movies.models.genre import Genre
from movies.utils.genre_name import GenreName


class FullGenreSerializer(serializers.ModelSerializer[Genre]):
    class Meta:
        id = serializers.ReadOnlyField()
        model = Genre
        fields = "__all__"

    def validate_name(self, genres):
        return [genre in GenreName.values() for genre in genres]

