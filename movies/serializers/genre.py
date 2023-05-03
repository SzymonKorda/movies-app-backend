from rest_framework import serializers

from movies.models.genre import Genre


class FullGenreSerializer(serializers.ModelSerializer[Genre]):
    class Meta:
        id = serializers.ReadOnlyField()
        model = Genre
        fields = "__all__"
