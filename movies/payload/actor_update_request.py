from datetime import date
from typing import TypedDict, Union


class ActorUpdateRequest(TypedDict, total=False):
    name: str
    biography: str
    place_of_birth: Union[str, None]
    birthday: Union[str, None]
    date_of_birth: Union[date, None]
    imdb_path: str
    poster_path: Union[str, None]
