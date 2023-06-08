from typing import List

from movies.payload.tmdb_actor_response import TmdbActorResponse
from movies.payload.tmdb_movie_credits_response import TmdbMovieCreditsResponse
from movies.payload.tmdb_movie_response import TmdbMovieResponse
from movies.payload.tmdb_movie_search_response import TmdbMovieSearchResponse
from movies.payload.tmdb_movie_trailer_response import TmdbMovieTrailerResponse
from movies.services.tmdb_interface import TmdbInterface


class FakeTmdbService(TmdbInterface):
    def fetch_movie(self, movie_id) -> TmdbMovieResponse:
        return TmdbMovieResponse(
            **{
                "original_title": "Forrest Gump",
                "overview": "Description",
                "budget": 55000000.0,
                "runtime": 142,
                "release_date": "1994-06-23",
                "poster_path": "/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
                "backdrop_path": "/3h1JZGDhZ8nzxdgvkxha0qBqi05.jpg",
                "adult": False,
                "imdb_id": "tt0109830",
                "revenue": 677387716.0,
                "status": "Released",
                "tagline": "The world will never be the same once you've seen it through the eyes of Forrest Gump.",
                "genres": [{"name": "Thriller"}, {"name": "RandomGenre"}],
            }
        )

    def fetch_actor(self, actor_id: int) -> TmdbActorResponse:
        return TmdbActorResponse(
            **{
                "name": "Christian Bale",
                "biography": "Description",
                "place_of_birth": "Haverfordwest, Pembrokeshire, Wales, UK",
                "birthday": "1974-01-30",
                "imdb_id": "nm0000288",
                "profile_path": "/qCpZn2e3dimwbryLnqxZuI88PTi.jpg",
            }
        )

    def fetch_movie_trailer(self, movie_id) -> List[TmdbMovieTrailerResponse]:
        return [
            TmdbMovieTrailerResponse(
                **{"site": "Youtube", "key": "0YAKkHutmFI", "official": True}
            ),
            TmdbMovieTrailerResponse(
                **{"site": "Youtube", "key": "0YAdsfsmFI", "official": False}
            ),
        ]

    def fetch_movie_credits(self, movie_id: int) -> TmdbMovieCreditsResponse:
        return TmdbMovieCreditsResponse(
            **{
                "cast": [
                    {
                        "id": 1,
                    },
                    {
                        "id": 2,
                    },
                    {
                        "id": 3,
                    },
                ],
                "crew": [
                    {"name": "Name1", "job": "Producer"},
                    {"name": "Name2", "job": "Director"},
                ],
            }
        )

    def movie_search(self, search_query) -> List[TmdbMovieSearchResponse]:
        return [
            TmdbMovieSearchResponse(
                **{
                    "title": "Forrest Gump",
                    "overview": "Description",
                    "poster_path": "/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
                }
            )
        ]
