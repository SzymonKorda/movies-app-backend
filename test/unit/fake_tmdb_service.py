from typing import Dict


class FakeTmdbService:
    responses: Dict[str, dict] = {}

    def clear_responses(self) -> None:
        self.responses.clear()

    def add_response(self, function: str, response: dict) -> None:
        self.responses[function] = response

    def fetch_movie(self, movie_id: int) -> dict:
        return self.responses.get("fetch_movie")

    def fetch_movie_trailer(self, movie_id: int) -> dict:
        return self.responses.get("fetch_movie_trailer")

    def fetch_movie_credits(self, movie_id: int) -> dict:
        return self.responses.get("fetch_movie_credits")

    def fetch_genre_list(self, movie_id: int) -> dict:
        return self.responses.get("fetch_genre_list")
