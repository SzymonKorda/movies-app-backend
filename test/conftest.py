import json

import pytest


RESOURCE_ID = 1
ENCODING = "utf-8"


@pytest.fixture
def tmdb_actor():
    return json.dumps(
        {
            "name": "Christian Bale",
            "biography": "Description",
            "place_of_birth": "Haverfordwest, Pembrokeshire, Wales, UK",
            "birthday": "1974-01-30",
            "imdb_id": "nm0000288",
            "profile_path": "/qCpZn2e3dimwbryLnqxZuI88PTi.jpg",
        }
    ).encode(ENCODING)


@pytest.fixture
def tmdb_resource_id() -> int:
    return RESOURCE_ID


@pytest.fixture
def tmdb_movie() -> bytes:
    return json.dumps(
        {
            "original_title": "Forrest Gump",
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
            "genres": [{"id": 1, "name": "Genre1"}, {"id": 2, "name": "Genre2"}],
        }
    ).encode(ENCODING)


@pytest.fixture
def tmdb_movie_trailer() -> bytes:
    return json.dumps(
        {
            "results": [
                {"site": "Youtube", "key": "0YAKkHutmFI", "official": True},
                {"site": "Youtube", "key": "0YAdsfsmFI", "official": False},
            ]
        }
    ).encode(ENCODING)


@pytest.fixture
def tmdb_movie_credits() -> bytes:
    return json.dumps(
        {
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
                {"name": "Name2", "job": "Director"},
            ],
        }
    ).encode(ENCODING)


@pytest.fixture
def tmdb_movie_search() -> bytes:
    return json.dumps(
        {
            "results": [
                {
                    "title": "Forrest Gump",
                    "overview": "Description",
                    "poster_path": "/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
                }
            ]
        }
    ).encode(ENCODING)
