import pytest
import json

from server import app, load_competitions, load_clubs
from unittest.mock import mock_open, patch


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def data_mock():
        competitions = [
            {"name": "Compétition 1", "date": "2026-03-27 10:00:00", "numberOfPlaces": "20"},
            {"name": "Compétition 2", "date": "2026-03-27 10:00:00", "numberOfPlaces": "22"}
        ]
        clubs = [
            {"name": "Club A", "email": "a@example.com", "points": "10"},
            {"name": "Club B", "email": "b@example.com", "points": "12"}
        ]

        return {
            'clubs': clubs,
            'competitions': competitions,
            'places': 12
        }

@pytest.fixture
def loaded_competitions(data_mock):
    test_daat_competitions = {
        "competitions": data_mock["competitions"]
    }
    mock_competitions = mock_open(read_data=json.dumps(test_daat_competitions))

    with patch("builtins.open", mock_competitions):
        competitions = load_competitions()
        assert competitions == test_daat_competitions["competitions"]

        for competition in competitions:
            assert "name" in competition
            assert "date" in competition
            assert "numberOfPlaces" in competition

        return competitions

@pytest.fixture
def loaded_clubs(data_mock):
    test_data_clubs = {
        "clubs": data_mock['clubs']
    }
    mock_clubs = mock_open(read_data=json.dumps(test_data_clubs))

    with patch("builtins.open", mock_clubs):
        clubs = load_clubs()
        assert clubs == test_data_clubs["clubs"]

        for club in clubs:
            assert "name" in club
            assert "email" in club
            assert "points" in club

        return clubs

