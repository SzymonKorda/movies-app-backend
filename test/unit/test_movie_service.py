from unittest import TestCase, mock

import pytest
from mock.mock import MagicMock
from pytest_mock import MockerFixture

import movies
from movies.services.movie_service import MovieService
from test.unit.fake_tmdb_service import FakeTmdbService


# movie_service = MovieService(FakeTmdbService())


@pytest.mark.django_db
def test_should_create_movie(
    mocker: MockerFixture,
    tmdb_movie_response,
    tmdb_movie_trailer,
    tmdb_movie_credits,
    resource_id,
):
    service = FakeTmdbService()
    movie_service = MovieService(service)
    service.clear_responses()

    service.add_response("fetch_movie", tmdb_movie_response)
    service.add_response("fetch_movie_trailer", tmdb_movie_trailer)
    service.add_response("fetch_movie_credits", tmdb_movie_credits)

    spy = mocker.spy(movie_service, "prepare_movie_data")

    result: dict = movie_service.create_movie(resource_id)

    assert spy.call_count == 1
