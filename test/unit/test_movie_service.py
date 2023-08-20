import pytest
from pytest_mock import MockerFixture
from rest_framework.exceptions import ValidationError

from movies.models import MovieGenre, Genre, Movie
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


# TODO: Find a way to spy call_count for movie_service_delete_movie.Movie.delete
@pytest.mark.django_db(reset_sequences=True)
def test_should_delete_movie(
    mocker: MockerFixture,
    movie_1,
    resource_id,
):
    # given
    movie_1.save()
    # spy = mocker.spy(movie_service, "movies.models.movie.delete")

    # when
    movie_service.delete_movie(resource_id)

    # then
    assert len(Movie.objects.all().values()) == 0
    # assert spy.call_count == 1


# TODO use spy instead of fetching all MovieGenre's from database
@pytest.mark.django_db(reset_sequences=True)
def test_should_add_valid_genres_to_movie(
    movie_1,
    tmdb_genre_list,
    tmdb_movie_response,
    resource_id,
):
    # given
    movie_1.save()
    prepare_genres(tmdb_genre_list)
    service.add_response("fetch_movie", tmdb_movie_response)

    # when
    movie_service.add_genres_to_movie(resource_id)

    # then
    result = list(MovieGenre.objects.all().values())
    movie_genres_id = {genre["genre_id"] for genre in result}
    assert len(movie_genres_id) == 3
    assert {4, 7, 14} == movie_genres_id


@pytest.mark.django_db(reset_sequences=True)
def test(
    movie_1,
    tmdb_genre_list,
    movie_genres_data,
    resource_id,
):
    # given
    movie_1.save()
    prepare_genres(tmdb_genre_list)
    prepare_movie_genres(movie_genres_data)

    # when
    result = movie_service.get_genres_from_movie(resource_id)
    genre_names = {genre["name"] for genre in result}

    # then
    assert {"Comedy", "Drama", "Romance"} == genre_names


def prepare_movie_genres(movie_genres_data):
    movie_genres = [
        MovieGenre(genre_id=genre["genre_id"], movie_id=genre["movie_id"])
        for genre in movie_genres_data["data"]
    ]
    MovieGenre.objects.bulk_create(movie_genres)


def prepare_genres(tmdb_genre_list):
    genres = [Genre(name=genre["name"]) for genre in tmdb_genre_list["genres"]]
    Genre.objects.bulk_create(genres)
