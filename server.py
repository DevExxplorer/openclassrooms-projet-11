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

    return render_template('welcome.html', club=club, competitions=competitions)

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
    found_competition = next((competition_item for competition_item in competitions if competition_item['name'] == competition), None)

    if not found_club or not found_competition:
        return render_template('index.html', error='Sorry, that club/competition wasn\'t found.'), 400

    return render_template(
        'booking.html',
        club=found_club,
        competition=found_competition
    )

def validate_places(places, competition_places, club_points):
    """
    Valide que la valeur donnée pour 'places' est un entier entre 1 et 12 inclus
    :param places: Nombre de places à valider.
    :raises ValueError: Si `places` n'est pas un entier ou n'est pas compris entre 1 et 12.
    """
    if not isinstance(places, int):
        raise ValueError("Le nombre de réservation doit être un entier")
    if not (1 <= places <= 12):
        raise ValueError("Le nombre de réservation doit être entre 1 et 12")
    if not places <= competition_places:
        raise ValueError(f'Tu ne peux pas réserver plus de {competition_places} places')
    if not places <= club_points:
        raise ValueError(f'Vous n\'avez pas assez de points, il ne vous en reste que { club_points } ')

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
    validate_places(places_required, competition_places, club_points)
    competition['numberOfPlaces'] = competition_places - places_required
    club['points'] = str(club_points - places_required)
    return club, competition

@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    """
   Gère la réservation de places pour une compétition via une requête POST.

   Récupère le club et la compétition à partir des données du formulaire.
   - Si le club ou la compétition n'existe pas, affiche un message d'erreur et retourne la page d'accueil avec un code 400.
   - Tente de convertir le nombre de places demandées en entier puis valide ce nombre via `validate_places`.
   - Si la validation échoue ou si la conversion échoue, affiche un message d'erreur et retourne la page d'accueil.
   - Si tout est valide, met à jour le nombre de places disponibles pour la compétition et affiche un message de succès.

   Retourne toujours la page 'welcome.html' avec les informations actualisées sur le club et les compétitions.
   """
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)

    if club is None or competition is None:
        flash("Club ou compétition introuvable.")
        return render_template('welcome.html', club=club, competitions=competitions), 400

    try:
        places_required = int(request.form['places'])
        competition_places = int(competition['numberOfPlaces'])
        club_points = int(club['points'])

        validate_places(places_required, competition_places, club_points)
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