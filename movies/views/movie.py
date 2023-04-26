from typing import Optional, List, Union

from django.db import transaction
from django.forms.models import model_to_dict
from django.http import HttpRequest, JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from movies.models.movie import Movie
from movies.serializers.movie import FullMovieSerializer, SimpleMovieSerializer
from movies.services.movie import MovieService


# TODO: ask about ReturnList, ReturnDict and serialized types (serializer.data)
class MovieView(APIView):
    movie_service: MovieService = MovieService()

    def get(self, request: HttpRequest, movie_id: Optional[int] = None) -> JsonResponse:
        if movie_id:
            movie: Movie = self.movie_service.get_movie(movie_id)
            return JsonResponse({'data': FullMovieSerializer(movie).data}, status=status.HTTP_200_OK)
        search_query: str = request.GET.get('search', default='')
        movies: List[Movie] = self.movie_service.get_all_movies(search_query)
        return JsonResponse({'data': SimpleMovieSerializer(movies, many=True).data}, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request: HttpRequest) -> JsonResponse:
        return self.movie_service.create_movie(request)

    def put(self, request: HttpRequest, movie_id: int) -> JsonResponse:
        movie = self.movie_service.update_movie(movie_id, request)
        if (movie == None):
            return JsonResponse({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(movie)

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


class MovieSearchView(APIView):
    movie_service = MovieService()

    def get(self, request):
        search_query = request.GET.get('query', '')
        return self.movie_service.movie_admin_search(search_query)
