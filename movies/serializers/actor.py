from rest_framework import serializers

from movies.models.actor import Actor


class FullActorSerializer(serializers.ModelSerializer[Actor]):
    class Meta:
        id = serializers.ReadOnlyField()
        model = Actor
        fields = '__all__'


class SimpleActorSerializer(serializers.ModelSerializer[Actor]):
    class Meta:
        id = serializers.ReadOnlyField()
        model = Actor
        fields = ('id', 'name', 'place_of_birth', 'date_of_birth', 'biography', 'poster_path')
