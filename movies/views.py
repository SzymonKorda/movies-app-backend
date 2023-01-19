from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from .models import Movie
from .serializers.movie import FullMovieSerializer, SimpleMovieSerializer


@api_view(['GET'])
def get_movie_list(request):
    movies = Movie.objects.all()
    movies_serializer = FullMovieSerializer(movies, many=True)
    return JsonResponse(movies_serializer.data, safe=False)


def get_movie(request, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
    movie_serializer = SimpleMovieSerializer(movie)
    return JsonResponse(movie_serializer.data)


@api_view(['POST'])
def create_movie(request):
    movie_data = JSONParser().parse(request)
    movies_serializer = FullMovieSerializer(data=movie_data)
    if movies_serializer.is_valid():
        movies_serializer.save()
        return JsonResponse(movies_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(movies_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
