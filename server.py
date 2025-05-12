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
    club = [club for club in clubs if club['email'] == email]

    if not email:
        return render_template(
            'index.html',
            error='Not email sent'
        )

    if club:
        return render_template(
            'welcome.html',
            club=club[0],
            competitions=competitions,
            date_competitions=check_date_competitions
        )
    else:
        return render_template(
            'index.html',
            error='Sorry, that email wasn\'t found.'
        )


@app.route('/book/<competition>/<club>')
def book(competition, club):
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
    # Donnée de la competition et du club séléctionné
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    # Gestion de la validation du formulaire
    places_required = int(request.form['places'])
    competition_places = int(competition['numberOfPlaces'])
    club_points = int(club['points'])

    if 0 < places_required <= 12:
        if places_required <= competition_places:
            if places_required <= club_points:
                competition['numberOfPlaces'] = competition_places - places_required
                club['points'] = str(int(club['points']) - places_required)
                flash('Votre réservation est validée !')
            else:
                flash(f'Vous n\'avez pas assez de points., il ne vous en reste que { club_points } ')
        else:
            flash(f'Tu ne peux pas réserver plus de {competition_places} places')
    else:
        flash('Vous ne pouvez réserver que 1 à 12 places par tournoi')

    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions,
        date_competitions=check_date_competitions
    )


def check_date_competitions(date_competition):
    competition_datetime = datetime.strptime(date_competition, "%Y-%m-%d %H:%M:%S")
    if competition_datetime < datetime.now():
        return 'La compétition est déjà passée'

    return


@app.route('/logout')
def logout():
    return redirect(url_for('index'))