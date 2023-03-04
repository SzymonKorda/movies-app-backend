from rest_framework import serializers

from ..models import Actor


class FullActorSerializer(serializers.ModelSerializer):
    class Meta:
        id = serializers.ReadOnlyField()
        model = Actor
        fields = ('id', 'first_name', 'last_name', 'born_place', 'born_year', 'description', 'image', 'movies', 'height')
        # extra_fields = ['movies']

        # https: // stackoverflow.com / a / 41063577
        # def get_field_names(self, declared_fields, info):
        #     expanded_fields = super(FullActorSerializer, self).get_field_names(declared_fields, info)
        #
        #     if getattr(self.Meta, 'extra_fields', None):
        #         return expanded_fields + self.Meta.extra_fields
        #     else:
        #         return expanded_fields


class SimpleActorSerializer(serializers.ModelSerializer):
    class Meta:
        id = serializers.ReadOnlyField()
        model = Actor
        fields = ('id', 'first_name', 'last_name', 'born_place', 'born_year', 'description', 'image', 'movies')
