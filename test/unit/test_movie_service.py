import pytest
from pytest_mock import MockerFixture
from rest_framework.exceptions import ValidationError

from movies.services.movie_service import MovieService
from test.unit.fake_tmdb_service import FakeTmdbService

service = FakeTmdbService()
movie_service = MovieService(service)


@pytest.mark.django_db
def test_should_create_movie_with_director_and_trailer_key(
    mocker: MockerFixture,
    cleanup,
    tmdb_movie_response,
    tmdb_movie_trailer,
    tmdb_movie_credits,
    resource_id,
    movie_response,
):
    # given
    service.clear_responses()
    service.add_response("fetch_movie", tmdb_movie_response)
    service.add_response("fetch_movie_trailer", tmdb_movie_trailer)
    service.add_response("fetch_movie_credits", tmdb_movie_credits)
    spy = mocker.spy(movie_service, "prepare_movie_data")

    # when
    result: dict = movie_service.create_movie(resource_id)

    # then
    assert spy.call_count == 1
    assert result == movie_response


@pytest.mark.django_db
def test_should_prepare_movie_data(
    tmdb_movie_response,
    tmdb_movie_trailer,
    tmdb_movie_credits,
    resource_id,
):
    # given
    service.clear_responses()
    service.add_response("fetch_movie", tmdb_movie_response)
    service.add_response("fetch_movie_trailer", tmdb_movie_trailer)
    service.add_response("fetch_movie_credits", tmdb_movie_credits)

    # when
    result: dict = movie_service.prepare_movie_data(resource_id)

    # then
    assert "crew" in result
    assert "cast" in result
    assert "results" in result


@pytest.mark.django_db
def test_should_throw_validation_error_when_to_title_from_response_is_present(
    cleanup,
    tmdb_movie_response,
    tmdb_movie_trailer,
    tmdb_movie_credits,
    resource_id,
):
    # given
    service.clear_responses()
    tmdb_movie_response["original_title"] = tmdb_movie_response.pop("title")
    service.add_response("fetch_movie", tmdb_movie_response)
    service.add_response("fetch_movie_trailer", tmdb_movie_trailer)
    service.add_response("fetch_movie_credits", tmdb_movie_credits)

    # when
    with pytest.raises(ValidationError) as e:
        movie_service.create_movie(resource_id)

    # then
    assert e.type is ValidationError
    assert e.value.detail['title'][0] == 'This field is required.'
