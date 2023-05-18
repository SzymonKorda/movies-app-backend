from typing import List
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from rest_framework.exceptions import NotFound

from movies.payload.tmdb_actor_response import TmdbActorResponse
from movies.payload.tmdb_movie_credits_response import TmdbMovieCreditsResponse
from movies.payload.tmdb_movie_response import TmdbMovieResponse
from movies.payload.tmdb_movie_search_response import TmdbMovieSearchResponse
from movies.payload.tmdb_movie_trailer_response import TmdbMovieTrailerResponse
from movies.services.tmdb import TmdbService


def test_should_raise_exception_when_tmdb_actor_not_found(
    mocker: MockerFixture, tmdb_resource_id: int
):
    mock_response: MagicMock = MagicMock()
    mock_response.status_code = 404
    mocker.patch("requests.get", return_value=mock_response)
    with pytest.raises(NotFound) as ex:
        TmdbService().fetch_actor(tmdb_resource_id)
    assert (
        ex.value.detail["detail"] == f"Tmdb actor with id {tmdb_resource_id} not found"
    )


def test_should_fetch_tmdb_actor(
    mocker: MockerFixture, tmdb_actor: bytes, tmdb_resource_id: int
):
    mock_response: MagicMock = MagicMock()
    mock_response.status_code = 200
    mock_response.content = tmdb_actor
    mocker.patch("requests.get", return_value=mock_response)
    result: TmdbActorResponse = TmdbService().fetch_actor(tmdb_resource_id)
    assert result.name == "Christian Bale"
    assert result.imdb_id == "nm0000288"


def test_should_fetch_tmdb_movie(
    mocker: MockerFixture, tmdb_movie: bytes, tmdb_resource_id: int
):
    mock_response: MagicMock = MagicMock()
    mock_response.status_code = 200
    mock_response.content = tmdb_movie
    mocker.patch("requests.get", return_value=mock_response)
    result: TmdbMovieResponse = TmdbService().fetch_movie(tmdb_resource_id)
    assert result.original_title == "Forrest Gump"
    assert result.imdb_id == "tt0109830"


def test_should_raise_exception_when_tmdb_movie_not_found(
    mocker: MockerFixture, tmdb_resource_id: int
):
    mock_response: MagicMock = MagicMock()
    mock_response.status_code = 404
    mocker.patch("requests.get", return_value=mock_response)
    with pytest.raises(NotFound) as ex:
        TmdbService().fetch_movie(tmdb_resource_id)
    assert (
        ex.value.detail["detail"] == f"Tmdb movie with id {tmdb_resource_id} not found"
    )


def test_should_fetch_movie_trailers(
    mocker: MockerFixture, tmdb_movie_trailer: bytes, tmdb_resource_id: int
):
    mock_response: MagicMock = MagicMock()
    mock_response.status_code = 200
    mock_response.content = tmdb_movie_trailer
    mocker.patch("requests.get", return_value=mock_response)
    result: List[TmdbMovieTrailerResponse] = TmdbService().fetch_movie_trailer(
        tmdb_resource_id
    )
    assert len(result) == 2
    assert result[0].key == "0YAKkHutmFI"
    assert result[1].official is False


def test_fetch_movie_credits(
    mocker: MockerFixture, tmdb_movie_credits: bytes, tmdb_resource_id: int
):
    mock_response: MagicMock = MagicMock()
    mock_response.status_code = 200
    mock_response.content = tmdb_movie_credits
    mocker.patch("requests.get", return_value=mock_response)
    result: TmdbMovieCreditsResponse = TmdbService().fetch_movie_credits(
        tmdb_resource_id
    )
    assert len(result.cast_members) == 3
    assert len(result.crew_members) == 2
    assert result.cast_members[0] == 1
    assert result.crew_members[1].job == "Director"


def test_movie_search(mocker: MockerFixture, tmdb_movie_search: bytes):
    mock_response: MagicMock = MagicMock()
    mock_response.status_code = 200
    mock_response.content = tmdb_movie_search
    mocker.patch("requests.get", return_value=mock_response)
    result: List[TmdbMovieSearchResponse] = TmdbService().movie_search("Gump")
    assert len(result) == 1
    assert result[0].title == "Forrest Gump"
    assert result[0].poster_path == "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg"
