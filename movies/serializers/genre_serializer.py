from rest_framework import serializers

from movies.models.genre import Genre
from movies.utils.genre_name import GenreName


class FullGenreSerializer(serializers.ModelSerializer[Genre]):
    class Meta:
        id = serializers.ReadOnlyField()
        model = Genre
        fields = ("name",)

    def validate_name(self, genre):
        return genre if genre in GenreName.values() else GenreName.OTHER