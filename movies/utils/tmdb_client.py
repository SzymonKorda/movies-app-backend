import urllib.parse

import requests
from django.conf import settings
from requests import Response, HTTPError
from rest_framework.exceptions import APIException


class TmdbClient:
    def __init__(self) -> None:
        self.base_uri = settings.TMDB_URI

    @classmethod
    def get_auth_headers(cls):
        return {"Authorization": f"Bearer {settings.TMDB_KEY}"}

    def get(self, path: str, params: dict = None) -> Response:
        return self.make_request("GET", path, params)

    def make_request(self, method: str, path: str, params: dict) -> Response:
        params = params if params else {}
        headers = self.get_auth_headers()

        response: Response = requests.request(
            method=method,
            url=urllib.parse.urljoin(self.base_uri, path),
            params=urllib.parse.urlencode(params),
            headers=headers,
        )
        self.handle_exception(response)
        return response

    # TODO: improve this
    def handle_exception(self, response: Response) -> None:
        try:
            response.raise_for_status()
        except HTTPError as e:
            raise APIException(e)
