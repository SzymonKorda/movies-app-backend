from dataclasses import dataclass
from typing import List

from movies.payload.tmdb_movie_crew_member_response import TmdbMovieCrewMemberResponse


@dataclass
class TmdbMovieCreditsResponse:
    cast_members: List[int]
    crew_members: List[TmdbMovieCrewMemberResponse]

    def __init__(self, **kwargs) -> None:
        self.cast_members = [member["id"] for member in kwargs["cast"]]
        self.crew_members = [
            TmdbMovieCrewMemberResponse(**member) for member in kwargs["crew"]
        ]
