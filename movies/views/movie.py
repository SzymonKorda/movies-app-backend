import json
import os
from datetime import datetime

import requests
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from movies.models.actor import Actor
from movies.models.genre import GenreType, Genre
from movies.models.movie import Movie
from movies.serializers.actor import FullActorSerializer, SimpleActorSerializer
from movies.serializers.genre import FullGenreSerializer
from movies.serializers.movie import FullMovieSerializer, SimpleMovieSerializer
from movies.services.movie import MovieService


class MovieView(APIView):
    movie_service = MovieService()

    def get(self, request, movie_id=None):
        if movie_id:
            return self.movie_service.get_movie(movie_id)
        return self.movie_service.get_all_movies()

    @transaction.atomic
    def post(self, request):
        return self.movie_service.create_movie(request)

    def put(self, request, movie_id):
        return self.movie_service.update_movie(movie_id, request)

    def delete(self, request, movie_id):
        return self.movie_service.delete_movie(movie_id)

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]


class MovieActorsView(APIView):
    def __init__(self, *args, **kwargs):
        self.movie_service = MovieService()
        super().__init__(*args, **kwargs)

    # permission_classes = [IsAuthenticated]

    def get(self, request, movie_id):
        return self.movie_service.get_movie_actors(movie_id)

    def post(self, request, movie_id, actor_id):
        return self.movie_service.add_actor_to_movie(actor_id, movie_id)


class MovieGenresView(APIView):
    def __init__(self, *args, **kwargs):
        self.movie_service = MovieService()
        super().__init__(*args, **kwargs)

    # permission_classes = [IsAuthenticated]

    def get(self, request, movie_id):
        return self.movie_service.get_movie_genres(movie_id)

