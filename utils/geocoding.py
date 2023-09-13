from geopy.geocoders import Nominatim
import re


def get_street_name_from_address(address):
    # Utilise une expression régulière pour extraire le nom de la rue
    pattern = r"\d+\.\s+(.+)$"  # Ce modèle capture tout après le premier chiffre suivi d'un point et d'un espace.
    match = re.search(pattern, address)
    if match:
        street_name = match.group(1)
        return street_name.strip()  # Supprime les espaces en début et fin, au cas où.
    else:
        return None


def get_lat_lng_from_address(address):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(get_street_name_from_address(address))
    if location:
        return location.latitude, location.longitude
    else:
        return None, None
