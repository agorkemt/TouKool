import random
from datetime import datetime, timedelta
from faker import Faker
from database import queries
from geopy.geocoders import Nominatim

from database.queries import adherents
from utils import adresses_37

fake = Faker('fr_FR')
geolocator = Nominatim(user_agent="geoapiExercises")

adresses = adresses_37.adresses


def get_coordinates_from_address(address):
    """Récupère les coordonnées à partir d'une adresse."""
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None, None


def generate_date_of_birth(min_age, max_age):
    """Génère une date de naissance pour une personne entre min_age et max_age."""
    today = datetime.today()
    birth_year = today.year - random.randint(min_age, max_age)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)  # Pour éviter les problèmes de jours en février
    return datetime(birth_year, birth_month, birth_day)


def generate_family():
    """Génère une famille avec une adresse commune."""
    nom_famille = fake.last_name()
    nombre_membres = random.randint(2, 5)
    famille = []

    full_address = random.choice(adresses)
    adresses.remove(full_address)
    latitude, longitude = get_coordinates_from_address(full_address)

    for _ in range(nombre_membres):
        prenom = fake.first_name()
        email = fake.email()
        genre = random.choice(["Homme", "Femme"])
        annee_adhesion = random.choice([2022, 2023])
        certificat_medical = random.choice([True, False])
        cotisation_payee = random.choice([True, False])

        if _ == 0:  # Assurez-vous qu'il y a au moins un adulte dans la famille
            date_naissance = generate_date_of_birth(18, 70)
        else:
            date_naissance = generate_date_of_birth(6, 70)

        if genre == "Homme":
            statut = random.choice(["Adulte", "Étudiant"])
        else:
            statut = random.choice(["Adulte", "Étudiant", "Demandeur d'emploi"])

        if statut == "Étudiant":
            cotisation = 5.0
        elif statut == "Demandeur d'emploi":
            cotisation = 8.0
        else:
            cotisation = 20.0

        adherent_data = {
            "nom": nom_famille,
            "prenom": prenom,
            "adresse_postale": full_address,
            "email": email,
            "genre": genre,
            "annee_adhesion": annee_adhesion,
            "certificat_medical": certificat_medical,
            "cotisation_payee": cotisation_payee,
            "latitude": latitude,
            "longitude": longitude,
            "statut": statut,
            "cotisation": cotisation,
            "date_naissance": date_naissance
        }
        famille.append(adherent_data)

    return famille


def generate_single():
    """Génère une personne seule avec une adresse unique."""
    nom = fake.last_name()
    prenom = fake.first_name()

    full_address = random.choice(adresses)
    adresses.remove(full_address)
    latitude, longitude = get_coordinates_from_address(full_address)

    email = fake.email()
    genre = random.choice(["Homme", "Femme"])
    annee_adhesion = random.choice([2022, 2023])
    certificat_medical = random.choice([True, False])
    cotisation_payee = random.choice([True, False])
    date_naissance = generate_date_of_birth(6, 70)

    if genre == "Homme":
        statut = random.choice(["Adulte", "Étudiant"])
    else:
        statut = random.choice(["Adulte", "Étudiant", "Demandeur d'emploi"])

    if statut == "Étudiant":
        cotisation = 5.0
    elif statut == "Demandeur d'emploi":
        cotisation = 8.0
    else:
        cotisation = 20.0

    adherent_data = {
        "nom": nom,
        "prenom": prenom,
        "adresse_postale": full_address,
        "email": email,
        "genre": genre,
        "annee_adhesion": annee_adhesion,
        "certificat_medical": certificat_medical,
        "cotisation_payee": cotisation_payee,
        "latitude": latitude,
        "longitude": longitude,
        "statut": statut,
        "cotisation": cotisation,
        "date_naissance": date_naissance
    }
    return adherent_data


def generate_adherents():
    """Génère soit une famille soit une personne seule."""
    if random.choice([True, False]):
        return generate_family()
    else:
        return [generate_single()]


def main():
    """Génère et ajoute des adhérents à la base de données."""
    nombre_adherents = 60
    adherentss = []

    for _ in range(nombre_adherents):
        adherentss.extend(generate_adherents())

    for adherent in adherentss:
        adherents.add_adherent(adherent)


if __name__ == "__main__":
    main()
