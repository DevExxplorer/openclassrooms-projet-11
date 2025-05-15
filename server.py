import json

from datetime import date, datetime

from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template(
        'index.html',
        clubs=clubs,
        error=''
    )

@app.route('/showSummary', methods=['POST'])
def show_summary():
    email = request.form.get('email')

    if not email:
        return render_template('index.html', error='No email sent'), 400

    loaded_clubs = load_clubs()
    loaded_competitions = load_competitions()

    club = next((club for club in loaded_clubs if club['email'] == email), None)

    if not club:
        return render_template('index.html', error='Sorry, that email wasn\'t found.'), 400

    return render_template(
        'welcome.html',
        club=club,
        competitions=loaded_competitions,
    )

# def check_date_competitions(date_competition):
#     if not date_competition:
#         return None
#
#     competition_datetime = datetime.strptime(date_competition, "%Y-%m-%d %H:%M:%S")
#
#     if competition_datetime < datetime.now():
#         return 'La compétition est déjà passée'
#
#     return None

@app.route('/book/<competition>/<club>')
def book(competition, club):
    print(f"Competition: {competition}, Club: {club}")
    print('TEST', clubs)
    found_club = next((club_item for club_item in clubs if club_item['name'] == club), None)
    found_competition = next((competition_item for competition_item in competitions if competition_item['name'] == competition), None)
    print(f"found_competition: {found_competition}, found_club: {found_club}")

    if not found_club or not found_competition:
        return redirect(url_for('index'))

    return render_template(
        'booking.html',
        club=found_club,
        competition=found_competition
    )

@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
    flash('Great-booking complete!')
    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions
    )


@app.route('/logout')
def logout():
    return redirect(url_for('index'))