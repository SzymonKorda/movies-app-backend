from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from movies.models import Movie, Actor


class MovieActorsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id, actor_id):
        return self.add_actor_to_movie(actor_id, movie_id)

    def add_actor_to_movie(self, actor_id, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
        try:
            actor = Actor.objects.get(pk=actor_id)
        except Actor.DoesNotExist:
            return JsonResponse({'message': 'Actor does not exist'}, status=status.HTTP_404_NOT_FOUND)
        movie.actors.add(actor)
        return JsonResponse({'message': 'Actor added to movie successfully'}, status=status.HTTP_200_OK)
