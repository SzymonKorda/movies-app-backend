from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from movies.models import Movie
from movies.serializers.movie import SimpleMovieSerializer, FullMovieSerializer


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