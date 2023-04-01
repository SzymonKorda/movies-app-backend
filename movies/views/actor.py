from django.db import connection
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from movies.models import Actor
from movies.serializers.actor import SimpleActorSerializer, FullActorSerializer


class ActorView(APIView):
    def get(self, request, actor_id=None):
        if actor_id:
            return self.get_actor(actor_id)
        return self.get_all_actors()

    def post(self, request):
        return self.create_actor(request)

    def put(self, request, actor_id):
        return self.update_actor(actor_id, request)

    def delete(self, request, actor_id):
        return self.delete_actor(actor_id)

    def get_all_actors(self):
        actors = Actor.objects.all()
        actor_serializer = SimpleActorSerializer(actors, many=True)
        return JsonResponse(actor_serializer.data, safe=False)

    def create_actor(self, request):
        actor_data = JSONParser().parse(request)
        actor_serializer = FullActorSerializer(data=actor_data)
        if actor_serializer.is_valid():
            actor_serializer.save()
            return JsonResponse(actor_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(actor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_actor(self, actor_id):
        try:
            actor = Actor.objects.get(pk=actor_id)
        except Actor.DoesNotExist:
            return JsonResponse({'message': 'Actor does not exist'}, status=status.HTTP_404_NOT_FOUND)

        actor.delete()
        return JsonResponse({'message': 'Actor was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    def update_actor(self, actor_id, request):
        try:
            actor = Actor.objects.get(pk=actor_id)
        except Actor.DoesNotExist:
            return JsonResponse({'message': 'Actor does not exist'}, status=status.HTTP_404_NOT_FOUND)

        actor_data = JSONParser().parse(request)
        actor_serializer = FullActorSerializer(actor, data=actor_data, partial=True)
        if actor_serializer.is_valid():
            actor_serializer.save()
            return JsonResponse(actor_serializer.data)
        return JsonResponse(actor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_actor(self, actor_id):
        try:
            actor = Actor.objects.get(pk=actor_id)
        except Actor.DoesNotExist:
            return JsonResponse({'message': 'Actor does not exist'}, status=status.HTTP_404_NOT_FOUND)

        actor_serializer = FullActorSerializer(actor)
        response_data = {}
        response_data.update(actor_serializer.data)
        response_data['movies'] = self.fetch_actor_movies(actor_id)
        return JsonResponse(response_data)


    def fetch_actor_movies(self, actor_id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT movie_id FROM movie_actors WHERE actor_id = %s", [actor_id])
            rows = cursor.fetchall()
        return rows


    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]