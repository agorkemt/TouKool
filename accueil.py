from datetime import datetime
from st_pages import Page, show_pages
from database.maintenance.maintenance import record_yearly_statistics, supprimer_adherents_annee_precedente, \
    check_and_record_statistics, check_and_delete_old_adherents
from database.mocks.generate_stats_for_past_years import generate_stats_for_past_years
from database.queries.adherents import get_number_adherents
from utils.countdown import countdown_to_october
from utils.helpers import LAST_YEAR, ACTUAL_YEAR
import streamlit as st
from database.queries.stats_history import get_all_statistiques, get_statistique_by_year
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Accueil",
    layout="wide"
)

show_pages([
    Page("accueil.py", "Acceuil"),
    Page("pages/1_gestion_adherents.py", "Gestion des adhésions"),
    Page("pages/2_cartographie.py", "Cartographie des adhérents")
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


def plot_pie_chart(data, title):
    fig, ax = plt.subplots(figsize=(6, 6))  # Définit la taille de la figure
    ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90,
           colors=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFD700', '#C71585'])
    ax.axis('equal')
    plt.title(title)
    return fig


def display_charts_for_year(year):
    stats = get_statistique_by_year(year)

    # Camembert pour le ratio homme/femme
    gender_data = {
        'Homme': stats.male_ratio,
        'Femme': stats.female_ratio
    }
    gender_fig = plot_pie_chart(gender_data, "Ratio Homme/Femme")

    # Camembert pour les statuts
    status_data = {
        'Adulte': stats.ratio_adulte,
        'Enfant': stats.ratio_enfant,
        'Étudiant': stats.ratio_etudiant,
        'Demandeur d\'emploi': stats.ratio_demandeur_emploi,
        'Ancien étudiant CEFIM': stats.ratio_ancien_etudiant_cefim,
        'Formateur CEFIM': stats.ratio_formateur_cefim
    }
    status_fig = plot_pie_chart(status_data, "Statuts")

    # Camembert pour le ratio famille
    family_data = {
        'Famille': stats.ratio_famille,
        'Non-Famille': 1 - stats.ratio_famille
    }
    family_fig = plot_pie_chart(family_data, "Ratio Famille")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.pyplot(gender_fig)
    with col2:
        st.pyplot(status_fig)
    with col3:
        st.pyplot(family_fig)


def main():
    display_header()
    display_metrics()
    check_and_record_statistics()
    check_and_delete_old_adherents()
    st.title("Statistiques")
    unique_years = sorted(list(set(s.year for s in get_all_statistiques())))
    year_to_display = st.selectbox("Choisir une année", options=unique_years)
    display_charts_for_year(year_to_display)


main()
