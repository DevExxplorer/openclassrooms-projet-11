import json
from datetime import date, datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    """
       Charge la liste des clubs à partir du fichier JSON 'clubs.json'.

       Ouvre le fichier 'clubs.json', lit les données JSON,
       puis retourne la liste associée à la clé 'clubs'.

       Returns:
           list: Liste des clubs chargés depuis le fichier JSON.
       """
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    """
       Charge la liste des compétitions à partir du fichier JSON 'competitions.json'.

       Ouvre le fichier 'competitions.json', lit les données JSON,
       puis retourne la liste associée à la clé 'competitions'.

       Returns:
           list: Liste des compétitions chargées depuis le fichier JSON.
       """
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()

# Dictionnaire pour tracker les réservations par club et par compétition
# Structure: {club_name: {competition_name: places_reserved}}
club_bookings = {}

@app.route('/')
def index():
    return render_template(
        'index.html',
        clubs=clubs,
        error=''
    )

def find_club_by_email(email, clubs_list):
    """
      Recherche un club dans une liste à partir de son adresse email.

      Args:
          email (str): L'email du club à rechercher.
          clubs_list (list): Liste des clubs, chaque club étant un dictionnaire contenant au moins la clé 'email'.

      Returns:
          dict or None: Le club correspondant à l'email, ou None si aucun club n'est trouvé.
      """
    return next((club for club in clubs_list if club['email'] == email), None)

@app.route('/showSummary', methods=['POST'])
def show_summary():
    """
        Route Flask pour afficher le résumé d'un club basé sur l'email fourni via un formulaire POST.

        Récupère l'email depuis le formulaire, cherche le club correspondant,
        puis affiche la page de bienvenue avec les détails du club et ses compétitions.

        Retourne une page d'erreur si l'email n'est pas fourni ou si le club n'est pas trouvé.

        Returns:
            Response: Page HTML rendue avec les informations du club ou un message d'erreur.
        """
    email = request.form.get('email')
    if not email:
        return render_template('index.html', error='No email sent'), 400

    club = find_club_by_email(email, clubs)

    if not club:
        return render_template('index.html', error='Sorry, that club wasn\'t found.'), 400

        # Ajout d'un champ 'is_active' à chaque compétition
    for competition in competitions:
        competition['is_active'] = check_date_competitions(competition.get('date')) is None

    return render_template('welcome.html', club=club, competitions=competitions)

def check_date_competitions(date_competition):
    if not date_competition:
        return None

    competition_datetime = datetime.strptime(date_competition, "%Y-%m-%d %H:%M:%S")

    if competition_datetime < datetime.now():
        return 'La compétition est déjà passée'

    return None

@app.route('/book/<competition>/<club>')
def book(competition, club):
    """
   Affiche la page de réservation pour une compétition donnée et un club donné.

   Recherche le club et la compétition par leur nom. Si l'un des deux n'est pas trouvé,
   affiche la page d'accueil avec un message d'erreur et un code HTTP 400.

   Args:
       competition (str): Nom de la compétition.
       club (str): Nom du club.

   Returns:
       Response: Page HTML de réservation si les deux existent, sinon page d'erreur.
   """
    found_club = next((club_item for club_item in clubs if club_item['name'] == club), None)
    found_competition = next(
        (competition_item for competition_item in competitions if competition_item['name'] == competition), None)

    if not found_club or not found_competition:
        return render_template('index.html', error='Sorry, that club/competition wasn\'t found.'), 400

    return render_template(
        'booking.html',
        club=found_club,
        competition=found_competition
    )

def get_club_bookings_for_competition(club_name, competition_name):
    """
    Récupère le nombre de places déjà réservées par un club pour une compétition donnée.

    Args:
        club_name (str): Nom du club
        competition_name (str): Nom de la compétition

    Returns:
        int: Nombre de places déjà réservées
    """
    if club_name not in club_bookings:
        return 0
    return club_bookings[club_name].get(competition_name, 0)

def update_club_bookings(club_name, competition_name, places_to_add):
    """
    Met à jour le tracking des réservations pour un club et une compétition.

    Args:
        club_name (str): Nom du club
        competition_name (str): Nom de la compétition
        places_to_add (int): Nombre de places à ajouter
    """
    if club_name not in club_bookings:
        club_bookings[club_name] = {}

    if competition_name not in club_bookings[club_name]:
        club_bookings[club_name][competition_name] = 0

    club_bookings[club_name][competition_name] += places_to_add

def validate_places(places, competition_places, club_points, club_name, competition_name):
    """
    Valide que la valeur donnée pour 'places' respecte toutes les contraintes
    :param places: Nombre de places à valider.
    :param competition_places: Nombre de places disponibles dans la compétition.
    :param club_points: Points disponibles du club.
    :param club_name: Nom du club.
    :param competition_name: Nom de la compétition.
    :raises ValueError: Si les contraintes ne sont pas respectées.
    """
    if not isinstance(places, int):
        raise ValueError("Le nombre de réservation doit être un entier")
    if not (1 <= places <= 12):
        raise ValueError("Le nombre de réservation doit être entre 1 et 12")
    if not places <= competition_places:
        raise ValueError(f'Tu ne peux pas réserver plus de {competition_places} places')
    if not places <= club_points:
        raise ValueError(f'Vous n\'avez pas assez de points, il ne vous en reste que {club_points}')

    # Nouvelle validation : vérifier la limite de 12 places par club par tournoi
    already_booked = get_club_bookings_for_competition(club_name, competition_name)
    total_after_booking = already_booked + places

    if total_after_booking > 12:
        remaining_slots = 12 - already_booked
        if remaining_slots <= 0:
            raise ValueError(f'Vous avez déjà réservé le maximum de 12 places pour ce tournoi')
        else:
            raise ValueError(
                f'Vous ne pouvez réserver que {remaining_slots} place(s) de plus pour ce tournoi (déjà réservé: {already_booked})')

def update_booking(places_required, club, competition):
    """
    Met à jour les places disponibles d'une compétition et les points d'un club après une réservation.

    Vérifie que le nombre de places demandé est valide, puis déduit ce nombre
    des places disponibles de la compétition ainsi que des points du club.

    Args:
        places_required (int): Nombre de places réservées.
        club (dict): Dictionnaire représentant le club, avec une clé 'points' (str).
        competition (dict): Dictionnaire représentant la compétition, avec une clé 'numberOfPlaces' (str ou int).

    Returns:
        tuple: Le club et la compétition mis à jour (dict, dict).
    """
    competition_places = int(competition['numberOfPlaces'])
    club_points = int(club['points'])

    validate_places(places_required, competition_places, club_points, club['name'], competition['name'])

    # Mettre à jour le tracking des réservations
    update_club_bookings(club['name'], competition['name'], places_required)

    competition['numberOfPlaces'] = competition_places - places_required
    club['points'] = str(club_points - places_required)
    return club, competition

@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)

    if club is None or competition is None:
        flash("Club ou compétition introuvable.")
        return render_template('welcome.html', club=club, competitions=competitions), 400

    try:
        places_required = int(request.form['places'])
        club, competition = update_booking(places_required, club, competition)
        flash('Great-booking complete!')
    except (ValueError, TypeError) as e:
        flash(str(e))
        return render_template('welcome.html', club=club, competitions=competitions)

    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions
    )

@app.route('/logout')
def logout():
    return redirect(url_for('index'))