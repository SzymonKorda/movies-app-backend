from typing import List, Dict, Union


class FakeTmdbService:
    responses: Dict[str, list] = {}

    def clear_responses(self):
        self.responses.clear()

    def add_response(self, function: str, response: Union[dict, List[dict]]):
        self.responses[function] = response

    def fetch_movie(self, movie_id):
        return self.responses["fetch_movie"].pop()

    def fetch_movie_trailer(self, movie_id):
        return self.responses['fetch_movie_trailer'].pop()

    def fetch_movie_credits(self, movie_id):
        return self.responses['fetch_movie_credits'].pop()

    def fetch_genre_list(self, movie_id):
        return self.responses['fetch_genre_list'].pop()


    # def add_movie_response(self, response):
    #     self.add_response('fetch_movie', response)
    #
    # def add_trailer_response(self, response):
    #     self.add_response('fetch_movie', response)


