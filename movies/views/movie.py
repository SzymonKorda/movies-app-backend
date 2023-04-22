from django.db import transaction
from rest_framework.views import APIView

from movies.services.movie import *


class MovieView(APIView):
    movie_service = MovieService()

    def get(self, request, movie_id=None):
        if movie_id:
            return self.movie_service.get_movie(movie_id)
        search_query = request.GET.get('search', '')
        return self.movie_service.get_all_movies(search_query)

    @transaction.atomic
    def post(self, request):
        return self.movie_service.create_movie(request)

    def put(self, request, movie_id):
        return self.movie_service.update_movie(movie_id, request)

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
