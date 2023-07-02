from unittest.mock import MagicMock, patch, PropertyMock

import pytest
from pytest_mock import MockerFixture
from rest_framework.exceptions import ValidationError

from movies.models import Movie, Actor
from movies.serializers.genre_serializer import FullGenreSerializer
from movies.services.movie_service import MovieService
from movies.services.tmdb_service import TmdbService
from movies.utils.genre_name import GenreName
from test.unit.fake_tmdb_service import FakeTmdbService

# movie_service = MovieService(FakeTmdbService())


@pytest.mark.django_db
def test_create_movie(
    mocker: MockerFixture,
    tmdb_movie_response,
    tmdb_movie_trailer,
    tmdb_movie_credits,
    resource_id,
    tmdb_genre_list,
):
    mocker.patch(
        "movies.apps.MoviesConfig.ready",
        return_value=None,
    )

    service = FakeTmdbService()
    movie_service = MovieService(service)

    service.clear_responses()

    service.add_response("fetch_movie", [tmdb_movie_response])
    service.add_response("fetch_movie_trailer", [tmdb_movie_trailer])
    service.add_response("fetch_movie_credits", [tmdb_movie_credits])
    # service.add_response("fetch_movie_genres", [tmdb_genre_list])

    movie_service.create_movie(resource_id)


# def test_fetch_movie(tmdb_movie_response):
# service.clear_responses()
#
# tmdb_movie_response.original_title = "Bububu"
# service.add_response("fetch_movie", tmdb_movie_response)
# service.add_response("add_movie_credits", tmdb_movie_response)
# service.add_response("fetch_trailer_movie", [tmdb_movie_response])
#
# movie = movie_service.create_movie(1)
