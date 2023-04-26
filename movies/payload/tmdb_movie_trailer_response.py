from dataclasses import dataclass


@dataclass
class TmdbMovieTrailerResponse:
    site: str
    key: str
    official: bool

    def __init__(self, **kwargs) -> None:
        self.site = kwargs['site']
        self.key = kwargs['key']
        self.official = kwargs['official']

