import json
import os
from typing import List, Union, Dict, Any

import requests
from requests import Response
from rest_framework.exceptions import APIException, NotFound

from movies.payload.tmdb_actor_response import TmdbActorResponse
from movies.payload.tmdb_movie_credits_response import TmdbMovieCreditsResponse
from movies.payload.tmdb_movie_response import TmdbMovieResponse
from movies.payload.tmdb_movie_search_response import TmdbMovieSearchResponse
from movies.payload.tmdb_movie_trailer_response import TmdbMovieTrailerResponse


class TmdbService:

    def __init__(self) -> None:
        self.tmdb_key = os.getenv('TMDB_KEY')
        self.tmdb_uri = 'https://api.themoviedb.org/3'
        self.headers = {'Authorization': 'Bearer ' + self.tmdb_key} if self.tmdb_key else None
        super().__init__()

    def fetch_actor(self, actor_id: int) -> TmdbActorResponse:
        response: Response = requests.get(self.tmdb_uri + '/person/' + str(actor_id), headers=self.headers)
        if response.status_code == 404:
            raise NotFound(detail={'detail': f'Tmdb actor with id {actor_id} not found'})
        return TmdbActorResponse(**json.loads(response.content))

    def fetch_movie(self, movie_id: int) -> TmdbMovieResponse:
        response: Response = requests.get(self.tmdb_uri + '/movie/' + str(movie_id), headers=self.headers)
        if response.status_code == 404:
            raise NotFound(detail={'detail': f'Tmdb movie with id {movie_id} not found'})
        return TmdbMovieResponse(**json.loads(response.content))

    def fetch_movie_trailer(self, movie_id) -> List[TmdbMovieTrailerResponse]:
        response: Response = requests.get(self.tmdb_uri + '/movie/' + str(movie_id) + '/videos', headers=self.headers)
        movie_trailers: Dict[str, Any] = json.loads(response.content)
        return [TmdbMovieTrailerResponse(**trailer) for trailer in movie_trailers['results']]

    def fetch_movie_credits(self, movie_id: int) -> TmdbMovieCreditsResponse:
        response: Response = requests.get(self.tmdb_uri + '/movie/' + str(movie_id) + '/credits', headers=self.headers)
        content: Dict[str, Any] = json.loads(response.content)
        return TmdbMovieCreditsResponse(**content)

    def movie_search(self, search_query) -> List[TmdbMovieSearchResponse]:
        params: Dict[str, str] = {'query': search_query}
        response: Response = requests.get(self.tmdb_uri + '/search/movie', params=params, headers=self.headers)
        return [TmdbMovieSearchResponse(**movie) for movie in json.loads(response.content)['results']]
