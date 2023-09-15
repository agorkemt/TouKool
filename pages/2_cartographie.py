import subprocess

import streamlit as st
import pydeck as pdk

from database.queries import adherents

# Récupérer les adhérents pour l'année 2023
adherents_2023 = adherents.get_adherents_by_year(2023)

# Préparer les données pour la carte
locations = [{"lat": adherent.latitude, "lon": adherent.longitude, "name": adherent.nom} for adherent in adherents_2023 if adherent.latitude and adherent.longitude]

# Créer la carte avec pydeck
if locations:
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state={
            'latitude': locations[0]['lat'],
            'longitude': locations[0]['lon'],
            'zoom': 9,
            'pitch': 50,
        },
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=locations,
                get_position=['lon', 'lat'],  # Modifiez 'lng' en 'lon' pour correspondre à vos données.
                auto_highlight=True,
                get_radius=1000,
                get_fill_color=[180, 0, 200, 140],
                pickable=True,
            ),
        ],
    ))
else:
    st.write("Aucun adhérent avec une adresse géocodée pour l'année 2023.")
