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
        date_competitions=check_date_competitions
    )

def check_date_competitions(date_competition):
    if not date_competition:
        return None

    competition_datetime = datetime.strptime(date_competition, "%Y-%m-%d %H:%M:%S")

    if competition_datetime < datetime.now():
        return 'La compétition est déjà passée'

    return None

@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = find_by_name(clubs, club)
    found_competition = find_by_name(competitions, competition)

    if not found_club or not found_competition:
        return redirect(url_for('index'))

    return render_template(
        'booking.html',
        club=found_club,
        competition=found_competition
    )


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    club_name = request.form.get('club')
    competition_name = request.form.get('competition')
    places_required = int(request.form.get('places', 0))

    competition = find_by_name(competitions, competition_name)
    if not competition:
        flash(f"La compétition {competition_name} n'a pas été trouvée.")
        return redirect(url_for('index'))

    club = find_by_name(clubs, club_name)
    if not club:
        flash(f"Le club {club_name} n'a pas été trouvé.")
        return redirect(url_for('index'))

    competition_places = int(competition['numberOfPlaces'])
    club_points = int(club['points'])

    if not (1 <= places_required <= 12):
        flash('Vous ne pouvez réserver que 1 à 12 places par tournoi.')
    elif places_required > competition_places:
        flash(f'Tu ne peux pas réserver plus de {competition_places} places.')
    elif places_required > club_points:
        flash(f'Pas assez de points. Il vous en reste {club_points}.')
    else:
        competition['numberOfPlaces'] = competition_places - places_required
        club['points'] = str(club_points - places_required)
        flash('Votre réservation est validée !')

    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions,
        date_competitions=check_date_competitions
    )


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

def find_by_name(items, name):
    return next((item for item in items if item['name'] == name), None)