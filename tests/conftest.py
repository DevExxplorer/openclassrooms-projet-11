import pytest
from unittest.mock import patch
import server
from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def data_mock():
    return {
        "clubs": [
            {"name": "Club 1", "email": "club1@example.com", "points": "10"},
            {"name": "Club 2", "email": "club2@example.com", "points": "5"},
        ],
        "competitions": [
            {"name": "Competition 1", "date": "2026-03-27 10:00:00", "numberOfPlaces": "20"},
            {"name": "Competition 2", "date": "2026-03-27 10:00:00", "numberOfPlaces": "20"}
        ]
    }


@pytest.fixture(autouse=True)
def patch_data(data_mock):
    with patch("server.load_clubs", return_value=data_mock["clubs"]), \
            patch("server.load_competitions", return_value=data_mock["competitions"]):

        server.clubs[:] = data_mock["clubs"]
        server.competitions[:] = data_mock["competitions"]

        yield
