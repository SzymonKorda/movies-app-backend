import json
import os
from typing import List

import requests
from requests import Response
from rest_framework.exceptions import APIException, NotFound

from movies.payload.tmdb_movie_response import TmdbMovieResponse
from movies.payload.tmdb_movie_trailer_response import TmdbMovieTrailerResponse


class TmdbService:

    def __init__(self) -> None:
        self.tmdb_key = os.getenv('TMDB_KEY')
        self.tmdb_uri = 'https://api.themoviedb.org/3'
        self.headers = {'Authorization': 'Bearer ' + self.tmdb_key}
        super().__init__()

    def fetch_actor(self, actor_id):
        actor_details_response = requests.get(self.tmdb_uri + '/person/' + str(actor_id), headers=self.headers)
        actor_details = json.loads(actor_details_response.content)
        return actor_details

    def fetch_movie(self, movie_id: int) -> TmdbMovieResponse:
        response: Response = requests.get(self.tmdb_uri + '/movie/' + str(movie_id), headers=self.headers)
        content: dict = json.loads(response.content)
        if response.status_code == 404:
            raise NotFound(detail={'detail': content['status_message']})
        return TmdbMovieResponse(**content)

    def fetch_movie_trailer(self, movie_id) -> List[TmdbMovieTrailerResponse]:
        movie_trailer_response: Response = requests.get(self.tmdb_uri + '/movie/' + str(movie_id) + '/videos',
                                                        headers=self.headers)
        movie_trailers: dict = json.loads(movie_trailer_response.content)
        return [TmdbMovieTrailerResponse(**trailer) for trailer in movie_trailers['results']]

    def fetch_movie_credits(self, movie_id):
        movie_credits_response = requests.get(self.tmdb_uri + '/movie/' + str(movie_id) + '/credits',
                                              headers=self.headers)
        return json.loads(movie_credits_response.content)

    def movie_search(self, search_query):
        params = {'query': search_query}
        search_result_response = requests.get(self.tmdb_uri + '/search/movie', params=params, headers=self.headers)
        return json.loads(search_result_response.content)['results']
