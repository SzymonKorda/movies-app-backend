from rest_framework import serializers
from movies.models import Genre


class FullGenreSerializer(serializers.ModelSerializer):
    class Meta:
        id = serializers.ReadOnlyField()
        model = Genre
        fields = '__all__'
