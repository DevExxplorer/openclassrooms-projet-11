from tests.conftest import data_mock


def test_load_clubs(loaded_clubs, data_mock):
    """
        Test that the load_clubs() function correctly reads club data
        from a mocked JSON file and returns a list of clubs
        with 'name', 'email', and 'points' keys.
    """
    assert loaded_clubs == data_mock['clubs']

