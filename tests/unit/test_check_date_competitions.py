# from datetime import timedelta, datetime
#
# from server import check_date_competitions
#
#
# def test_check_date_competitions():
#     assert check_date_competitions(None) is None
#     assert check_date_competitions("") is None
#
#     past_date = "2020-01-01 10:00:00"
#     assert check_date_competitions(past_date) == 'La compétition est déjà passée'
