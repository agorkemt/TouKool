import random
from faker import Faker
from database import queries
from geopy.geocoders import Nominatim

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


def generate_family():
    """Génère une famille avec une adresse commune."""
    nom_famille = fake.last_name()
    nombre_membres = random.randint(2, 5)
    famille = []

    # Choisissez une adresse de la liste et supprimez-la pour éviter les doublons
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

        # Ajoutez le statut et la cotisation en fonction des critères de votre choix
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
            "statut": statut,  # Ajoutez le statut
            "cotisation": cotisation  # Ajoutez la cotisation
        }
        famille.append(adherent_data)

    return famille


def generate_single():
    """Génère une personne seule avec une adresse unique."""
    nom = fake.last_name()
    prenom = fake.first_name()

    # Choisissez une adresse de la liste et supprimez-la pour éviter les doublons
    full_address = random.choice(adresses)
    adresses.remove(full_address)
    latitude, longitude = get_coordinates_from_address(full_address)

    email = fake.email()
    genre = random.choice(["Homme", "Femme"])
    annee_adhesion = random.choice([2022, 2023])
    certificat_medical = random.choice([True, False])
    cotisation_payee = random.choice([True, False])

    # Ajoutez le statut et la cotisation en fonction des critères de votre choix
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
        "statut": statut,  # Ajoutez le statut
        "cotisation": cotisation  # Ajoutez la cotisation
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
    adherents = []

    for _ in range(nombre_adherents):
        adherents.extend(generate_adherents())

    for adherent in adherents:
        queries.add_adherent(adherent)


if __name__ == "__main__":
    main()
