import urllib.parse

import requests
from requests import Response, HTTPError
from requests.auth import AuthBase
from rest_framework.exceptions import APIException


class ApiClient:
    def __init__(self, base_uri) -> None:
        self.base_uri = base_uri
        super().__init__()

    def get(self, *path, auth: AuthBase, **params) -> Response:
        return self.make_request(*path, method="GET", auth=auth, **params)

    def make_request(self, *path, method: str, auth: AuthBase, **params) -> Response:
        response: Response = requests.request(
            method=method,
            url=self.prepare_uri(*path),
            params=urllib.parse.urlencode(params),
            auth=auth,
        )
        self.handle_exception(response)
        return response

    # TODO: improve this
    def handle_exception(self, response: Response) -> None:
        try:
            response.raise_for_status()
        except HTTPError as e:
            raise APIException(e)

    # TODO: use urljoin() method
    def prepare_uri(self, *path) -> str:
        uri = self.base_uri
        for p in path:
            uri = "{}/{}".format(uri, p)
        return uri
