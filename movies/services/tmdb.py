import json
import os

import requests


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

    def fetch_movie(self, movie_id):
        movie_details_response = requests.get(self.tmdb_uri + '/movie/' + str(movie_id), headers=self.headers)
        return json.loads(movie_details_response.content)

    def fetch_movie_trailer(self, movie_id):
        movie_trailer_response = requests.get(self.tmdb_uri + '/movie/' + str(movie_id) + '/videos', headers=self.headers)
        movie_trailer = json.loads(movie_trailer_response.content)
        return movie_trailer

    def fetch_movie_credits(self, movie_id):
        movie_credits_response = requests.get(self.tmdb_uri + '/movie/' + str(movie_id) + '/credits', headers=self.headers)
        return json.loads(movie_credits_response.content)

