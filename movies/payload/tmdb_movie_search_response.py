from dataclasses import dataclass
from typing import Union


@dataclass
class TmdbMovieSearchResponse:
    title: str
    poster_path: Union[str, None]

    def __init__(self, **kwargs) -> None:
        self.title = kwargs["title"]
        poster_path: Union[str, None] = kwargs["poster_path"]
        self.poster_path = (
            "https://image.tmdb.org/t/p/w500" + poster_path if poster_path else None
        )
