from django.conf import settings
from requests import models
from requests.auth import AuthBase


class TmdbAuth(AuthBase):
    def __init__(self) -> None:
        self.headers = settings.TMDB_HEADERS
        super().__init__()

    def __call__(self, r: models.PreparedRequest) -> models.PreparedRequest:
        r.headers.update(self.headers)
        return r
