from unittest.mock import MagicMock, patch, PropertyMock

import pytest
from pytest_mock import MockerFixture
from rest_framework.exceptions import ValidationError

from movies.models import Movie, Actor
from movies.services.movie_service import MovieService
from test.unit.fake_tmdb_service import FakeTmdbService

movie_service = MovieService(FakeTmdbService())


def test_should_create_movie(
    mocker: MockerFixture, movie: Movie, resource_id: int, tmdb_actor
):
    mocker.patch(
        "movies.serializers.movie_serializer.FullMovieSerializer.is_valid",
        return_value=True,
    )
    mocker.patch(
        "movies.serializers.movie_serializer.FullMovieSerializer.save",
        return_value=movie,
    )

    mocker.patch(
        "movies.serializers.movie_serializer.FullMovieSerializer.data",
        return_value=movie,
    )

    mocker.patch(
        "movies.services.genre_service.GenreService.find_or_create_genre",
        return_value={"name": "Thriller"},
    )

    result = movie_service.create_movie(resource_id)

    assert len(result["genres"]) == 0


# def test_should_create_movie_x(
#     mocker: MockerFixture, movie: Movie, resource_id: int, tmdb_actor
# ):
#     mocker.patch(
#         "movies.serializers.movie_serializer.FullMovieSerializer.is_valid",
#         return_value=False,
#         side_effect=ValidationError(detail={"non_field_errors": ["error"]}),
#     )
#
#     movie_service.create_movie(resource_id)
