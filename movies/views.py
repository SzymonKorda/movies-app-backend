from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Movie, Actor
from .serializers.actor import FullActorSerializer, SimpleActorSerializer
from .serializers.jwt_response import CustomTokenObtainPairSerializer
from .serializers.movie import FullMovieSerializer, SimpleMovieSerializer
from .serializers.user import UserSerializer


class MovieView(APIView):
    def get(self, request, movie_id=None):
        if movie_id:
            return self.get_movie(movie_id)
        return self.get_all_movies()

    def post(self, request):
        return self.create_movie(request)

    def put(self, request, movie_id):
        return self.update_movie(movie_id, request)

    def delete(self, request, movie_id):
        return self.delete_movie(movie_id)

    def get_all_movies(self):
        movies = Movie.objects.all()
        movies_serializer = SimpleMovieSerializer(movies, many=True)
        return JsonResponse(movies_serializer.data, safe=False)

    def delete_movie(self, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return JsonResponse({'message': 'Movie was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    def update_movie(self, movie_id, request):
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
        movie_data = JSONParser().parse(request)
        movie_serializer = FullMovieSerializer(movie, data=movie_data, partial=True)
        if movie_serializer.is_valid():
            movie_serializer.save()
            return JsonResponse(movie_serializer.data)
        return JsonResponse(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_movie(self, request):
        movie_data = JSONParser().parse(request)
        movie_serializer = FullMovieSerializer(data=movie_data)
        if movie_serializer.is_valid():
            movie_serializer.save()
            return JsonResponse(movie_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_movie(self, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
        movie_serializer = FullMovieSerializer(movie)
        return JsonResponse(movie_serializer.data)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]


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
        return JsonResponse(actor_serializer.data)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]


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


class ActorMoviesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id, actor_id):
        return self.add_movie_to_actor(actor_id, movie_id)

    def add_movie_to_actor(self, actor_id, movie_id):
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


class UserView(APIView):
    def post(self, request):
        return self.create_user(request)

    def create_user(self, request):
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
