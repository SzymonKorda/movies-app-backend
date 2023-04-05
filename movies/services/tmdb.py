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

