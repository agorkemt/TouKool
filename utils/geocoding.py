from geopy.geocoders import Nominatim
import re


def get_street_name_from_address(address):
    pattern = r"\d+\.\s+(.+)$"
    match = re.search(pattern, address)
    if match:
        street_name = match.group(1)
        return street_name.strip()
    else:
        return None


def get_lat_lng_from_address(address):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(get_street_name_from_address(address))
    if location:
        return location.latitude, location.longitude
    else:
        return None, None
