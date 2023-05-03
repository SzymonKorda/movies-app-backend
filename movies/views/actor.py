from typing import Optional

from django.http import JsonResponse, HttpRequest
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import APIView

from movies.services.actor import ActorService


class ActorView(APIView):

    def __init__(self, *args, **kwargs):
        self.actor_service = ActorService()
        super().__init__(*args, **kwargs)

    def get(self, request: HttpRequest, actor_id: Optional[int] = None) -> JsonResponse:
        if actor_id:
            actor: ReturnDict = self.actor_service.get_actor(actor_id)
            return JsonResponse({'data': actor}, status=status.HTTP_200_OK)
        actors: ReturnDict = self.actor_service.get_all_actors()
        return JsonResponse({'data': actors}, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest) -> JsonResponse:
        actor: ReturnDict = self.actor_service.create_actor(request)
        return JsonResponse({'data': actor}, status=status.HTTP_201_CREATED)

    def put(self, request: HttpRequest, actor_id: int) -> JsonResponse:
        actor: ReturnDict = self.actor_service.update_actor(actor_id, request)
        return JsonResponse({'data': actor}, status=status.HTTP_200_OK)

    def delete(self, request: HttpRequest, actor_id: int) -> JsonResponse:
        self.actor_service.delete_actor(actor_id)
        return JsonResponse({'message': 'Actor was deleted successfully!'}, status=status.HTTP_200_OK)

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]


class ActorMoviesView(APIView):

    def __init__(self, *args, **kwargs):
        self.actor_service = ActorService()
        super().__init__(*args, **kwargs)

    # permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, actor_id: int):
        movies: ReturnDict = self.actor_service.get_movies_from_actor(actor_id)
        return JsonResponse({'data': movies}, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest, movie_id: int, actor_id: int) -> JsonResponse:
        self.actor_service.add_movie_to_actor(actor_id, movie_id)
        return JsonResponse({'message': 'Actor added to movie successfully'}, status=status.HTTP_200_OK)
