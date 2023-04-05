from datetime import datetime
import json
import os

import requests
from django.db import connection
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from movies.models.actor import Actor
from movies.models.movie import Movie
from movies.serializers.actor import SimpleActorSerializer, FullActorSerializer
from movies.serializers.movie import SimpleMovieSerializer
from movies.services.actor import ActorService


class ActorView(APIView):

    def __init__(self, *args, **kwargs):
        self.actor_service = ActorService()
        super().__init__(*args, **kwargs)

    def get(self, request, actor_id=None):
        if actor_id:
            return self.actor_service.get_actor(actor_id)
        return self.actor_service.get_all_actors()

    def post(self, request):
        return self.actor_service.create_actor(request)

    def put(self, request, actor_id):
        return self.actor_service.update_actor(actor_id, request)

    def delete(self, request, actor_id):
        return self.actor_service.delete_actor(actor_id)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]


class ActorMoviesView(APIView):

    def __init__(self, *args, **kwargs):
        self.actor_service = ActorService()
        super().__init__(*args, **kwargs)

    # permission_classes = [IsAuthenticated]

    def get(self, request, actor_id):
        return self.actor_service.get_movies_from_actor(actor_id)

    def post(self, request, movie_id, actor_id):
        return self.actor_service.add_movie_to_actor(actor_id, movie_id)
