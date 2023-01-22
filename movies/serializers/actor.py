from rest_framework import serializers

from ..models import Actor


class FullActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class SimpleActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'first_name', 'last_name', 'height', 'born_year')
