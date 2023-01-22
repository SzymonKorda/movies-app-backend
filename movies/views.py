from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from .serializers.actor import FullActorSerializer, SimpleActorSerializer
from .models import Movie, Actor
from .serializers.movie import FullMovieSerializer, SimpleMovieSerializer


@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        return get_all_movies()
    elif request.method == 'POST':
        return create_movie(request)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return get_movie(movie)
    elif request.method == 'PUT':
        return update_movie(movie, request)
    elif request.method == 'DELETE':
        return delete_movie(movie)


@api_view(['GET', 'POST'])
def actor_list(request):
    if request.method == 'GET':
        return get_all_actors()
    if request.method == 'POST':
        return create_actor(request)


@api_view(['GET', 'PUT', 'DELETE'])
def actor_detail(request, actor_id):
    try:
        actor = Actor.objects.get(pk=actor_id)
    except Actor.DoesNotExist:
        return JsonResponse({'message': 'Actor does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return get_actor(actor)
    elif request.method == 'PUT':
        return update_actor(actor, request)
    elif request.method == 'DELETE':
        return delete_actor(actor)


@api_view(['POST'])
def movie_actors(request, movie_id, actor_id):
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


@api_view(['POST'])
def actor_movies(request, actor_id, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)

    try:
        actor = Actor.objects.get(pk=actor_id)
    except Actor.DoesNotExist:
        return JsonResponse({'message': 'Actor does not exist'}, status=status.HTTP_404_NOT_FOUND)

    actor.movie_set.add(movie)
    return JsonResponse({'message': 'Movie added to actor successfully'}, status=status.HTTP_200_OK)


def create_actor(request):
    actor_data = JSONParser().parse(request)
    actor_serializer = FullActorSerializer(data=actor_data)
    if actor_serializer.is_valid():
        actor_serializer.save()
        return JsonResponse(actor_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(actor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_all_actors():
    actors = Actor.objects.all()
    actor_serializer = SimpleActorSerializer(actors, many=True)
    return JsonResponse(actor_serializer.data, safe=False)


def delete_actor(actor):
    actor.delete()
    return JsonResponse({'message': 'Actor was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


def update_actor(actor, request):
    actor_data = JSONParser().parse(request)
    actor_serializer = FullActorSerializer(actor, data=actor_data, partial=True)
    if actor_serializer.is_valid():
        actor_serializer.save()
        return JsonResponse(actor_serializer.data)
    return JsonResponse(actor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_actor(actor):
    actor_serializer = FullActorSerializer(actor)
    return JsonResponse(actor_serializer.data)


def delete_movie(movie):
    movie.delete()
    return JsonResponse({'message': 'Movie was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


def update_movie(movie, request):
    movie_data = JSONParser().parse(request)
    movie_serializer = FullMovieSerializer(movie, data=movie_data, partial=True)
    if movie_serializer.is_valid():
        movie_serializer.save()
        return JsonResponse(movie_serializer.data)
    return JsonResponse(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_movie(movie):
    movie_serializer = FullMovieSerializer(movie)
    return JsonResponse(movie_serializer.data)


def get_all_movies():
    movies = Movie.objects.all()
    movies_serializer = SimpleMovieSerializer(movies, many=True)
    return JsonResponse(movies_serializer.data, safe=False)


def create_movie(request):
    movie_data = JSONParser().parse(request)
    movie_serializer = FullMovieSerializer(data=movie_data)
    if movie_serializer.is_valid():
        movie_serializer.save()
        return JsonResponse(movie_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
