from typing import List

from movies.payload.tmdb_actor_response import TmdbActorResponse
from movies.payload.tmdb_movie_credits_response import TmdbMovieCreditsResponse
from movies.payload.tmdb_movie_response import TmdbMovieResponse
from movies.payload.tmdb_movie_search_response import TmdbMovieSearchResponse
from movies.payload.tmdb_movie_trailer_response import TmdbMovieTrailerResponse


class TmdbInterface:
    def fetch_actor(self, actor_id: int) -> TmdbActorResponse:
        pass

    def fetch_movie(self, movie_id: int) -> TmdbMovieResponse:
        pass

    def fetch_movie_trailer(self, movie_id) -> List[TmdbMovieTrailerResponse]:
        pass

    def fetch_movie_credits(self, movie_id: int) -> TmdbMovieCreditsResponse:
        pass

    def movie_search(self, search_query) -> List[TmdbMovieSearchResponse]:
        pass
