class TmdbMovieCrewMemberResponse:
    name: str
    job: str

    def __init__(self, **kwargs) -> None:
        self.name = kwargs['name']
        self.job = kwargs['job']
