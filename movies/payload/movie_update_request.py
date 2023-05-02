from datetime import date
from typing import TypedDict, Union


class MovieUpdateRequest(TypedDict, total=False):
    title: str
    description: str
    box_office: float
    duration: Union[int, None]
    release_date: date
    poster_path: Union[str, None]
    backdrop_path: Union[str, None]
    adult: bool
    imdb_path: Union[str, None]
    revenue: float
    status: str
    tagline: Union[str, None]
