import pytest

from server import app, load_competitions, load_clubs


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def data_mock():
        competition = [
            {
                "name": "Test Competition",
                "date": "2025-06-01 10:00:00",
                "numberOfPlaces": "30"
            }
        ]
        club = [
            {
                "name": "Test Club",
                "email": "test@club.com",
                "points": "20"
            }
        ]

        return {
            'club': club,
            'competition': competition,
            'places': 12
        }