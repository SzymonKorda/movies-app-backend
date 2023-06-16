from movies.utils.tmdb_client import TmdbClient


class TmdbService:
    def __init__(self) -> None:
        self.client = TmdbClient()
        super().__init__()

    def fetch_actor(self, actor_id: int) -> dict:
        return self.client.get(path=f"person/{actor_id}").json()

    def fetch_movie(self, movie_id: int) -> dict:
        return self.client.get(path=f"movie/{movie_id}").json()

    def fetch_movie_trailer(self, movie_id) -> dict:
        return self.client.get(path=f"movie/{movie_id}/videos").json()

    def fetch_movie_credits(self, movie_id: int) -> dict:
        return self.client.get(path=f"movie/{movie_id}/credits").json()

    def movie_search(self, search_query) -> dict:
        return self.client.get(
            path=f"search/movie", params={"query": search_query}
        ).json()

    def fetch_genre_list(self) -> dict:
        return self.client.get(path="genre/movie/list").json()
