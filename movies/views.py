from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from .models import Movie
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
    movies_serializer = FullMovieSerializer(data=movie_data)
    if movies_serializer.is_valid():
        movies_serializer.save()
        return JsonResponse(movies_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(movies_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
