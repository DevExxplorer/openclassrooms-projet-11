import json
from tkinter.messagebox import RETRY

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
    return render_template('index.html', error='')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    email = request.form.get('email')
    club = [club for club in clubs if club['email'] == email]

    if not email:
        return render_template(
            'index.html',
            error='Not email sent'
        )

    if club:
        return render_template('welcome.html', club=club[0], competitions=competitions)
    else:
        return render_template(
            'index.html',
            error='Sorry, that email wasn\'t found.'
        )



@app.route('/book/<competition>/<club>')
def book(competition, club):
    competitions = load_competitions()
    clubs = load_clubs()

    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]

    if found_club and found_competition:
        return render_template(
            'booking.html',
            club=found_club,
            competition=found_competition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
        )


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competitions = load_competitions()
    clubs = load_clubs()

    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
    display_points(club, places_required)
    flash('Great-booking complete!')
    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions,
        data_json=places_required
    )


def display_points(club, places_required):
    club['points'] = int(club['points']) - places_required
    return club


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
