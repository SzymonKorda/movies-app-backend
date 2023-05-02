from dataclasses import dataclass
from typing import List, Union


@dataclass
class TmdbMovieResponse:
    adult: bool
    backdrop_path: Union[str, None]
    budget: int
    genres: List[str]
    imdb_id: Union[str, None]
    original_title: str
    overview: str
    poster_path: Union[str, None]
    release_date: str
    revenue: int
    runtime: Union[int, None]
    status: str
    tagline: Union[str, None]

    def __init__(self, **kwargs) -> None:
        self.adult = kwargs['adult']
        self.backdrop_path = kwargs['backdrop_path']
        self.budget = kwargs['budget']
        self.genres = [genre['name'] for genre in kwargs['genres']]
        self.imdb_id = kwargs['imdb_id']
        self.original_title = kwargs['original_title']
        self.overview = kwargs['overview']
        self.poster_path = kwargs['poster_path']
        self.release_date = kwargs['release_date']
        self.revenue = kwargs['revenue']
        self.runtime = kwargs['runtime']
        self.status = kwargs['status']
        self.tagline = kwargs['tagline']






