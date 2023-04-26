from dataclasses import dataclass


@dataclass
class GenreResponse:
    id: int
    name: str

    def __init__(self, **kwargs) -> None:
        self.id

