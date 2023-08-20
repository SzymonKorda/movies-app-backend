import pytest
from pytest_mock import MockerFixture
from rest_framework.exceptions import ValidationError

from movies.services.movie_service import MovieService
from test.unit.fake_tmdb_service import FakeTmdbService

service = FakeTmdbService()
movie_service = MovieService(service)


@pytest.mark.django_db(reset_sequences=True)
def test_should_create_movie_with_director_and_trailer_key(
    mocker: MockerFixture,
    cleanup,
    tmdb_movie_response,
    tmdb_movie_trailer,
    tmdb_movie_credits,
    resource_id,
    created_movie_response,
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
    assert result == created_movie_response


@pytest.mark.django_db
def test_should_prepare_movie_data_to_create_movie(
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
    assert e.value.detail["title"][0] == "This field is required."


@pytest.mark.django_db(reset_sequences=True)
def test_should_get_full_movie_data(
    movie_1, get_full_movie_1_response, resource_id, cleanup
):
    # given
    movie_1.save()

    # when
    result = movie_service.get_movie(resource_id)

    # then
    assert result == get_full_movie_1_response


@pytest.mark.django_db(reset_sequences=True)
def test_should_get_simple_all_movie_data(
    movie_1,
    movie_2,
    movie_3,
    get_simple_movie_1_response,
    get_simple_movie_2_response,
    get_simple_movie_3_response,
    cleanup,
):
    # given
    movie_1.save()
    movie_2.save()
    movie_3.save()

    # when
    result = movie_service.get_all_movies()

    # then
    assert dict(result[0]) == get_simple_movie_1_response
    assert dict(result[1]) == get_simple_movie_2_response
    assert dict(result[2]) == get_simple_movie_3_response


@pytest.mark.django_db(reset_sequences=True)
def test_should_update_movie_title_and_poster_key(
    movie_1,
    movie_1_valid_update_request,
    get_full_movie_1_response,
    resource_id,
):
    # given
    movie_1.save()
    get_full_movie_1_response.update(
        [
            ("title", movie_1_valid_update_request["title"]),
            ("poster_key", movie_1_valid_update_request["poster_key"]),
        ]
    )

    # when
    result = movie_service.update_movie(resource_id, movie_1_valid_update_request)

    # then
    assert result == get_full_movie_1_response


@pytest.mark.django_db(reset_sequences=True)
def test_should_throw_validation_error_when_title_is_not_valid_string(
    movie_1,
    movie_1_invalid_update_request,
    resource_id,
):
    # given
    movie_1.save()

    # when
    with pytest.raises(ValidationError) as e:
        movie_service.update_movie(resource_id, movie_1_invalid_update_request)

    # then
    assert e.type is ValidationError
    assert e.value.detail["title"][0] == "Not a valid string."
