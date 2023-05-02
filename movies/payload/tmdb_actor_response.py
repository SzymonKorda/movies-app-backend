from dataclasses import dataclass
from typing import Union


@dataclass
class TmdbActorResponse:
    name: str
    biography: str
    place_of_birth: Union[str, None]
    birthday: Union[str, None]
    imdb_id: str
    profile_path: Union[str, None]

    def __init__(self, **kwargs) -> None:
        self.name = kwargs['name']
        self.biography = kwargs['biography']
        self.place_of_birth = kwargs['place_of_birth']
        self.birthday = kwargs['birthday']
        self.imdb_id = kwargs['imdb_id']
        self.profile_path = kwargs['profile_path']

