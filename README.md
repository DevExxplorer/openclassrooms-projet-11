# gudlift-registration

## 1. Pourquoi

Il s'agit d'un projet de preuve de concept (POC) pour montrer une version allégée de notre plateforme de réservation de compétitions. L'objectif est de garder les choses aussi légères que possible et d'utiliser les retours des utilisateurs pour itérer.

## 2. Pour commencer

Ce projet utilise les technologies suivantes :

- **Python v3.x+**
- **Flask** - Alors que Django fait beaucoup de choses pour nous dès le départ, Flask nous permet d'ajouter uniquement ce dont nous avons besoin.
- **[Environnement virtuel](https://virtualenv.pypa.io/en/stable/installation.html)** - Cela garantit que vous pourrez installer les bons packages sans interférer avec Python sur votre machine. Avant de commencer, assurez-vous de l'avoir installé globalement.

## 3. Installation

- Après le clonage, accédez au répertoire et tapez `virtualenv .`. Cela configurera un environnement Python virtuel dans ce répertoire.

- Ensuite, tapez `source bin/activate`. Vous devriez voir que votre invite de commande a changé pour afficher le nom du dossier. Cela signifie que vous pouvez installer des packages ici sans affecter les fichiers à l'extérieur. Pour désactiver, tapez `deactivate`.

- Plutôt que de chercher les packages dont vous avez besoin, vous pouvez les installer en une seule étape. Tapez `pip install -r requirements.txt`. Cela installera tous les packages listés dans le fichier respectif. Si vous installez un package, assurez-vous que les autres le sachent en mettant à jour le fichier requirements.txt. Un moyen simple de le faire est `pip freeze > requirements.txt`.

- Flask nécessite que vous définissiez une variable d'environnement pour le fichier Python. Vous devrez définir le fichier comme étant `server.py`. Consultez [ici](https://flask.palletsprojects.com/en/latest/quickstart/) pour plus de détails.

- Vous devriez maintenant être prêt à tester l'application. Dans le répertoire, tapez soit `flask run` soit `python -m flask run`. L'application devrait répondre avec une adresse à laquelle vous devriez pouvoir accéder via votre navigateur.

## 4. Configuration actuelle

L'application est alimentée par des fichiers JSON. C'est pour éviter d'avoir une base de données jusqu'à ce que nous en ayons réellement besoin. Les principaux sont :

- **competitions.json** - liste des compétitions
- **clubs.json** - liste des clubs avec les informations pertinentes. Vous pouvez regarder ici pour voir quelles adresses e-mail l'application acceptera pour la connexion.

## 5. Tests

Ce projet utilise **pytest** comme framework de test. Pytest offre une syntaxe simple et des fonctionnalités puissantes pour écrire et exécuter des tests.

Nous utilisons également **coverage** pour mesurer la couverture de code et nous assurer que nos tests couvrent correctement l'ensemble de l'application.

## 6. Liens vers ressources externes

- [Documentation officielle Flask](https://flask.palletsprojects.com/)
- [Guide d'utilisation pytest](https://docs.pytest.org/)
- [Documentation coverage](https://coverage.readthedocs.io/)
- [Guide des environnements virtuels Python](https://virtualenv.pypa.io/en/stable/)
- [Bonnes pratiques Flask](https://flask.palletsprojects.com/en/latest/patterns/)

## 7. Configurations particulières

### Variables d'environnement
Créez un fichier `.env` à la racine du projet avec :
```
FLASK_APP=server.py
FLASK_DEBUG=1
```

### Structure des fichiers JSON

**competitions.json** :
```json
{
    "competitions": [
        {
            "name": "Spring Festival",
            "date": "2026-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]
}
```

**clubs.json** :
```json
{
    "clubs": [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        }
    ]
}
```

## 8. Conventions de nommage

### Structure des fichiers et dossiers
```
gudlift-registration/
├── server.py              # Point d'entrée Flask
├── requirements.txt       # Dépendances Python
├── .env                  # Variables d'environnement
├── pytest.ini            # Configuration pytest
├── .coveragerc           # Configuration coverage
├── competitions.json     # Données des compétitions
├── clubs.json           # Données des clubs
├── templates/           # Templates HTML
├── tests/               # Tous les tests
│   ├── conftest.py     # Configuration des tests
│   ├── functional/     # Tests de bout en bout
│   ├── integration/    # Tests d'intégration
│   ├── performance/    # Tests de performance (Locust)
│   └── unit/          # Tests unitaires
└── README.md           # Ce fichier
```

### Conventions pour les tests
- Tous les fichiers de test doivent commencer par `test_`
- Les classes de test doivent commencer par `Test`
- Les fonctions de test doivent commencer par `test_`

## Commandes utiles

### Exécuter l'application
```bash
flask run
```

### Exécuter les tests
```bash
# Tous les tests
pytest

# Tests avec coverage
pytest --cov=. --cov-report=html

# Tests spécifiques
pytest tests/unit/
pytest tests/integration/
pytest tests/functional/
```

### Tests de performance
```bash
locust -f tests/performance/locustfile.py
```