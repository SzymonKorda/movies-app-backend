import json
import os
from typing import List, Dict, Any

import requests
from requests import Response, HTTPError
from rest_framework.exceptions import NotFound, APIException

from django.conf import settings

from movies.payload.tmdb_actor_response import TmdbActorResponse
from movies.payload.tmdb_movie_credits_response import TmdbMovieCreditsResponse
from movies.payload.tmdb_movie_response import TmdbMovieResponse
from movies.payload.tmdb_movie_search_response import TmdbMovieSearchResponse
from movies.payload.tmdb_movie_trailer_response import TmdbMovieTrailerResponse


class TmdbService:

    # TODO: auth object, and passed to request
    # https://requests.readthedocs.io/en/latest/user/authentication/
    def __init__(self) -> None:
        # self.tmdb_key = os.getenv("TMDB_KEY")
        self.tmdb_key = settings.TMDB_KEY
        self.tmdb_uri = "https://api.themoviedb.org/3"
        self.headers = (
            {"Authorization": "Bearer " + self.tmdb_key} if self.tmdb_key else None
        )
        super().__init__()

    def fetch_actor(self, actor_id: int) -> TmdbActorResponse:
        response: Response = requests.get(
            self.tmdb_uri + "/person/" + str(actor_id), headers=self.headers
        )
        if response.status_code == 404:
            raise NotFound(
                detail={"detail": f"Tmdb actor with id {actor_id} not found"}
            )
        return TmdbActorResponse(**json.loads(response.content))

    def make_request(self, method: str, path: str) -> Response:
        response: Response = requests.request(
            method, self.tmdb_uri + "/" + path, headers=self.headers
        )
        try:
            response.raise_for_status()
        except HTTPError as e:
            raise APIException(e)

    def fetch_movie(self, movie_id: int) -> TmdbMovieResponse:
        response: Response = self.make_request("get", f"movie/{movie_id}")

        # response: Response = requests.get(
        #     self.tmdb_uri + "/movie/" + str(movie_id), headers=self.headers
        # )

        # if response.status_code == 404:
        #     raise NotFound(
        #         detail={"detail": f"Tmdb movie with id {movie_id} not found"}
        #     )
        return TmdbMovieResponse(**response.json())
        # return TmdbMovieResponse(**json.loads(response.content))

    def fetch_movie_trailer(self, movie_id) -> List[TmdbMovieTrailerResponse]:
        response: Response = requests.get(
            self.tmdb_uri + "/movie/" + str(movie_id) + "/videos", headers=self.headers
        )
        movie_trailers: Dict[str, Any] = json.loads(response.content)
        return [
            TmdbMovieTrailerResponse(**trailer) for trailer in movie_trailers["results"]
        ]

    def fetch_movie_credits(self, movie_id: int) -> TmdbMovieCreditsResponse:
        response: Response = requests.get(
            self.tmdb_uri + "/movie/" + str(movie_id) + "/credits", headers=self.headers
        )
        content: Dict[str, Any] = json.loads(response.content)
        return TmdbMovieCreditsResponse(**content)

    def movie_search(self, search_query) -> List[TmdbMovieSearchResponse]:
        params: Dict[str, str] = {"query": search_query}
        response: Response = requests.get(
            self.tmdb_uri + "/search/movie", params=params, headers=self.headers
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