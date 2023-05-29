import json
from typing import List, Dict, Any

from django.conf import settings
from requests import Response

from movies.payload.tmdb_actor_response import TmdbActorResponse
from movies.payload.tmdb_movie_credits_response import TmdbMovieCreditsResponse
from movies.payload.tmdb_movie_response import TmdbMovieResponse
from movies.payload.tmdb_movie_search_response import TmdbMovieSearchResponse
from movies.payload.tmdb_movie_trailer_response import TmdbMovieTrailerResponse
from movies.utils.api_client import ApiClient
from movies.utils.tmdb_auth import TmdbAuth


class TmdbService:
    def __init__(self) -> None:
        self.client = ApiClient(settings.TMDB_URI)
        self.auth = TmdbAuth()
        super().__init__()

    def fetch_actor(self, actor_id: int) -> TmdbActorResponse:
        response: Response = self.client.get("person", f"{actor_id}", auth=self.auth)
        return TmdbActorResponse(**json.loads(response.content))

    def fetch_movie(self, movie_id: int) -> TmdbMovieResponse:
        response: Response = self.client.get("movie", f"{movie_id}", auth=self.auth)
        return TmdbMovieResponse(**response.json())

    def fetch_movie_trailer(self, movie_id) -> List[TmdbMovieTrailerResponse]:
        response: Response = self.client.get(
            "movie", f"{movie_id}", "videos", auth=self.auth
        )
        movie_trailers: Dict[str, Any] = json.loads(response.content)
        return [
            TmdbMovieTrailerResponse(**trailer) for trailer in movie_trailers["results"]
        ]

    def fetch_movie_credits(self, movie_id: int) -> TmdbMovieCreditsResponse:
        response: Response = self.client.get(
            "movie", f"{movie_id}", "credits", auth=self.auth
        )
        content: Dict[str, Any] = json.loads(response.content)
        return TmdbMovieCreditsResponse(**content)

    def movie_search(self, search_query) -> List[TmdbMovieSearchResponse]:
        params: Dict[str, str] = {"query": search_query}
        response: Response = self.client.get(
            "search", "movie", auth=self.auth, **params
        )
        return [
            TmdbMovieSearchResponse(**movie)
            for movie in json.loads(response.content)["results"]
        ]


# TODO: create fake manager - whole service mock, list of requests
# FakeTestService
# requests = []
# FakeTestService.add_request()
# Jakub Korda18:11
# T,bbService.get_movies()
