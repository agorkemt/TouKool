import streamlit as st
from st_pages import Page, show_pages
from database.maintenance.maintenance import check_and_record_statistics, check_and_delete_old_adherents
from database.queries.adherents import get_number_adherents
from templates.gestion_adherents import run_gestion_adherent
from utils.countdown import countdown_to_october
from utils.helpers import LAST_YEAR, ACTUAL_YEAR
from database.queries.stats_history import get_statistique_by_year

# Configuration de Streamlit
st.set_page_config(
    page_title="Accueil",
    layout="wide"
)


def display_header():
    """Affiche l'en-tête de la page."""

    # Utilisez des colonnes pour centrer le contenu.
    # Les colonnes 1 et 5 agissent comme des "marges" pour centrer le contenu.
    col1, col2, col3, col4, col5 = st.columns([1, 2, 6, 2, 1])


    with col3:
        with st.container():
            col_img, col_text = st.columns([2, 8])
            with col_img:
                st.image("static/image/logo.png", width=100)
            with col_text:
                st.write("# TouKoul")

        st.markdown("<div style='padding: 50px;'></div>", unsafe_allow_html=True)  # Espace de 50px
        display_metrics()


def display_metrics():
    """Affiche les métriques sur la page."""
    st.empty()  # Espace entre le header et les métriques
    with st.container():
        adherents_this_year = get_number_adherents()
        adherents_last_year = get_statistique_by_year(LAST_YEAR).adherent_count
        delta_adherents = adherents_this_year - adherents_last_year

        days_remaining = countdown_to_october()

        col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 2, 2, 2, 1])  # Colonnes pour centrer les métriques
        with col2:
            col2.metric(f"Fin de saison {LAST_YEAR}", f"{days_remaining} jours")
        with col3:
            col3.metric(f"Adhérents saison {LAST_YEAR}", f"{adherents_last_year}")
        with col4:
            col4.metric(f"Adhérents saison {ACTUAL_YEAR}", f"{adherents_this_year}", delta_adherents)

def main():
    show_pages([
        Page("accueil.py", "Acceuil"),
        Page("pages/2_cartographie.py", "Cartographie des adhérents"),
        Page("pages/3_statistiques.py", "Statistiques"),
        Page("pages/4_historiques.py", "Historique"),
    ])

    display_header()
    check_and_record_statistics()
    check_and_delete_old_adherents()
    run_gestion_adherent()


if __name__ == "__main__":
    main()
