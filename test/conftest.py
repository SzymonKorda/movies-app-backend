import datetime
import random

import pytest

from movies.models.movie import Movie
from movies.payload.tmdb_actor_response import TmdbActorResponse

RESOURCE_ID = 1
ENCODING = "utf-8"
MOVIE_TITLE_SEARCH_QUERY = "Gump"


@pytest.fixture
def tmdb_actor() -> TmdbActorResponse:
    return TmdbActorResponse(
        **{
            "id": random.randint(1, 100),
            "name": "Christian Bale",
            "biography": "Description",
            "place_of_birth": "Haverfordwest, Pembrokeshire, Wales, UK",
            "birthday": "1974-01-30",
            "imdb_id": "nm0000288",
            "profile_path": "/qCpZn2e3dimwbryLnqxZuI88PTi.jpg",
        }
    )


@pytest.fixture
def resource_id() -> int:
    return RESOURCE_ID


@pytest.fixture
def cleanup() -> None:
    yield
    # This is executed when the test using the fixture is done
    Movie.objects.all().delete()


@pytest.fixture
def tmdb_movie_response() -> dict:
    return {
        "title": "Forrest Gump",
        "overview": "Description",
        "budget": 55000000.0,
        "runtime": 142,
        "release_date": "1994-06-23",
        "poster_path": "/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
        "backdrop_path": "/3h1JZGDhZ8nzxdgvkxha0qBqi05.jpg",
        "adult": False,
        "imdb_id": "tt0109830",
        "revenue": 677387716.0,
        "status": "Released",
        "tagline": "The world will never be the same once you've seen it through the eyes of Forrest Gump.",
    }


@pytest.fixture
def movie_1() -> Movie:
    return Movie(
        **{
            "title": "Forrest Gump",
            "description": "Description",
            "box_office": 55000000.0,
            "duration": 142,
            "release_date": datetime.date(1994, 6, 23),
            "poster_key": "/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
            "backdrop_key": "/3h1JZGDhZ8nzxdgvkxha0qBqi05.jpg",
            "adult": False,
            "imdb_key": "tt0109830",
            "revenue": 677387716.0,
            "status": "Released",
            "tagline": "The world will never be the same once you've seen it through the eyes of Forrest Gump.",
            "trailer_key": "0YAKkHutmFI",
            "director": "Robert Zemeckis",
        }
    )


@pytest.fixture
def movie_2():
    return Movie(
        **{
            "title": "Oppenheimer",
            "description": "The story of J. Robert Oppenheimer’s role in the development of the atomic bomb during World War II.",
            "box_office": 100000000.0,
            "duration": 181,
            "release_date": datetime.date(2023, 7, 19),
            "poster_key": "/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
            "backdrop_key": "/rLb2cwF3Pazuxaj0sRXQ037tGI1.jpg",
            "adult": False,
            "imdb_key": "tt15398776",
            "revenue": 671426709.0,
            "status": "Released",
            "tagline": "The world forever changes.",
            "trailer_key": "e25RoI3rykw",
            "director": "Christopher Nolan",
        }
    )


@pytest.fixture
def movie_3():
    return Movie(
        **{
            "title": "Barbie",
            "description": "Barbie and Ken are having the time of their lives in the colorful and seemingly perfect world of Barbie Land. However, when they get a chance to go to the real world, they soon discover the joys and perils of living among humans.",
            "box_office": 145000000.0,
            "duration": 114,
            "release_date": datetime.date(2023, 7, 19),
            "poster_key": "/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg",
            "backdrop_key": "/nHf61UzkfFno5X1ofIhugCPus2R.jpg",
            "adult": False,
            "imdb_key": "tt1517268",
            "revenue": 1202507382.0,
            "status": "Released",
            "tagline": "She's everything. He's just Ken.",
            "trailer_key": "74Ie5QZC3Mc",
            "director": "Greta Gerwig",
        }
    )


@pytest.fixture
def created_movie_response() -> dict:
    return {
        "id": 1,
        "title": "Forrest Gump",
        "description": "Description",
        "box_office": 55000000.0,
        "duration": 142,
        "release_date": datetime.date(1994, 6, 23),
        "poster_key": "/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
        "backdrop_key": "/3h1JZGDhZ8nzxdgvkxha0qBqi05.jpg",
        "adult": False,
        "imdb_key": "tt0109830",
        "revenue": 677387716.0,
        "status": "Released",
        "tagline": "The world will never be the same once you've seen it through the eyes of Forrest Gump.",
        "director": "Robert Zemeckis",
        "trailer_key": "0YAKkHutmFI",
    }


@pytest.fixture
def get_full_movie_1_response() -> dict:
    return {
        "id": 1,
        "title": "Forrest Gump",
        "description": "Description",
        "box_office": 55000000.0,
        "duration": 142,
        "release_date": "1994-06-23",
        "poster_key": "/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
        "backdrop_key": "/3h1JZGDhZ8nzxdgvkxha0qBqi05.jpg",
        "adult": False,
        "imdb_key": "tt0109830",
        "revenue": 677387716.0,
        "status": "Released",
        "tagline": "The world will never be the same once you've seen it through the eyes of Forrest Gump.",
        "director": "Robert Zemeckis",
        "trailer_key": "0YAKkHutmFI",
    }


@pytest.fixture
def get_simple_movie_1_response() -> dict:
    return {
        "id": 1,
        "title": "Forrest Gump",
        "description": "Description",
        "release_date": "1994-06-23",
        "duration": 142,
        "poster_key": "/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
    }


@pytest.fixture
def get_simple_movie_2_response() -> dict:
    return {
        "id": 2,
        "title": "Oppenheimer",
        "description": "The story of J. Robert Oppenheimer’s role in the development of the atomic bomb during World War II.",
        "duration": 181,
        "release_date": "2023-07-19",
        "poster_key": "/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
    }


@pytest.fixture
def get_simple_movie_3_response() -> dict:
    return {
        "id": 3,
        "title": "Barbie",
        "release_date": "2023-07-19",
        "description": "Barbie and Ken are having the time of their lives in the colorful and seemingly perfect world of Barbie Land. However, when they get a chance to go to the real world, they soon discover the joys and perils of living among humans.",
        "duration": 114,
        "poster_key": "/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg",
    }


@pytest.fixture
def tmdb_movie_trailer() -> dict:
    return {
        "results": [
            {"site": "Youtube", "key": "0YAKkHutmFI", "official": True},
            {"site": "Youtube", "key": "0YAdsfsmFI", "official": False},
        ]
    }


@pytest.fixture
def tmdb_movie_credits() -> dict:
    return {
        "cast": [
            {
                "id": 1,
            },
            {
                "id": 2,
            },
            {
                "id": 3,
            },
        ],
        "crew": [
            {"name": "Name1", "job": "Producer"},
            {"name": "Robert Zemeckis", "job": "Director"},
        ],
    }


@pytest.fixture
def tmdb_genre_list() -> dict:
    return {
        "genres": [
            {"name": "Action"},
            {"name": "Adventure"},
            {"name": "Animation"},
            {"name": "Comedy"},
            {"name": "Crime"},
            {"name": "Documentary"},
            {"name": "Drama"},
            {"name": "Family"},
            {"name": "Fantasy"},
            {"name": "History"},
            {"name": "Horror"},
            {"name": "Music"},
            {"name": "Mystery"},
            {"name": "Romance"},
            {"name": "Science Fiction"},
            {"name": "TV Movie"},
            {"name": "Thriller"},
            {"name": "War"},
            {"name": "Western"},
        ]
    }


# @pytest.fixture
# def tmdb_movie_search() -> bytes:
#     return json.dumps(
#         {
#             "results": [
#                 {
#                     "title": "Forrest Gump",
#                     "overview": "Description",
#                     "poster_path": "/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
#                 }
#             ]
#         }
#     ).encode(ENCODING)


@pytest.fixture
def search_query() -> str:
    return MOVIE_TITLE_SEARCH_QUERY
