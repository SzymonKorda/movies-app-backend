from unittest.mock import MagicMock

import pytest
from django.conf import settings
from pytest_mock import MockerFixture
from requests.models import HTTPError
from rest_framework.exceptions import APIException

from movies.utils.api_client import ApiClient

api_client = ApiClient(settings.TMDB_URI)


def test_should_raise_api_exception(mocker: MockerFixture):
    method_mock: MagicMock = mocker.patch(
        "requests.models.Response.raise_for_status", side_effect=HTTPError()
    )
    response_mock: MagicMock = MagicMock(raise_for_status=method_mock, status_code=404)

    with pytest.raises(APIException) as e:
        api_client.handle_exception(response_mock)

    # TODO why isInstance(e.type, APIException does not work, also why
    #  e.type is APIException works)
    assert isinstance(e.value, APIException)


def test_should_prepare_valid_uri(resource_id):
    result = api_client.prepare_uri("movies", f"{resource_id}", "actors")
    assert result == "https://api.themoviedb.org/3/movies/1/actors"
