from typing import List
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from rest_framework.exceptions import NotFound

from movies.models.movie import Movie
from movies.payload.tmdb_movie_response import TmdbMovieResponse
from movies.services.movie_service import MovieService


def test_should_get_movie(mocker: MockerFixture, movie: Movie, resource_id: int):
    mock_response: MagicMock = MagicMock()
    mock_response.content = movie
    mock: MagicMock = mocker.patch(
        "movies.models.movie.Movie.objects.get", return_value=mock_response
    )

    MovieService().get_movie(resource_id)

    mock.assert_called_once()


def test_should_raise_exception_when_movie_does_not_exist(
    mocker: MockerFixture, resource_id: int
):
    mocker.patch(
        "movies.models.movie.Movie.objects.get", side_effect=Movie.DoesNotExist
    )

    with pytest.raises(NotFound) as ex:
        MovieService().get_movie(resource_id)

    assert ex.value.detail["detail"] == f"Movie with id {resource_id} does not exist"


def test_should_get_all_movies(mocker: MockerFixture, movie: Movie, search_query):
    mocker.patch(
        "movies.models.movie.Movie.objects.filter", return_value=[movie, movie]
    )

    result: List[Movie] = MovieService().get_all_movies(search_query)

    assert len(result) == 2
    assert search_query in result[0].title


def test_should_create_movie(
    mocker: MockerFixture, resource_id: int, tmdb_movie: TmdbMovieResponse
):

    mock_response = mocker.patch(
        "movies.services.tmdb.TmdbService.fetch_movie", return_value=tmdb_movie
    )

    MovieService().create_movie(resource_id)
