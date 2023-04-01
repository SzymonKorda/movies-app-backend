from rest_framework import serializers

from ..models import Actor


class FullActorSerializer(serializers.ModelSerializer):
    class Meta:
        id = serializers.ReadOnlyField()
        model = Actor
        fields = '__all__'
        # fields = [field.name for field in model._meta.fields]
        # fields.append('movies')
        # fields = ('id', 'name', 'place_of_birth', 'date_of_birth', 'biography', 'poster_path', 'imdb_id')
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
        fields = ('id', 'name', 'place_of_birth', 'date_of_birth', 'biography', 'poster_path')
