from st_pages import Page, show_pages
from database.maintenance.maintenance import check_and_record_statistics, check_and_delete_old_adherents
from database.mocks.generate_stats_for_past_years import generate_stats_for_past_years
from database.queries.adherents import get_number_adherents
from utils.countdown import countdown_to_october
from utils.helpers import LAST_YEAR, ACTUAL_YEAR
import streamlit as st
from database.queries.stats_history import  get_statistique_by_year

st.set_page_config(
    page_title="Accueil",
    layout="wide"
)

show_pages([
    Page("accueil.py", "Acceuil"),
    Page("pages/1_gestion_adherents.py", "Gestion des adhésions"),
    Page("pages/2_cartographie.py", "Cartographie des adhérents"),
    Page("pages/3_statistiques.py", "Statistiques"),
    Page("pages/4_historiques.py", "Historique"),
])


def display_header():
    col1, col2 = st.columns([2, 8])
    with col1:
        st.image("static/image/logo.png", width=100)
    with col2:
        st.write("# TouKoul")


def display_metrics():
    with st.container():
        adherents_this_year = get_number_adherents()
        adherents_last_year = get_statistique_by_year(LAST_YEAR).adherent_count
        delta_adherents = adherents_this_year - adherents_last_year

        days_remaining = countdown_to_october()

        col1m, col2m, col3m = st.columns(3)
        col1m.metric(f"Fin de saison {LAST_YEAR}", f"{days_remaining} jours")
        col2m.metric(f"Adhérents saison {LAST_YEAR}", f"{adherents_last_year}")
        col3m.metric(f"Adhérents saison {ACTUAL_YEAR}", f"{adherents_this_year}", delta_adherents)


def main():
    display_header()
    display_metrics()
    check_and_record_statistics()
    check_and_delete_old_adherents()


main()
generate_stats_for_past_years()
