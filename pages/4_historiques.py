import streamlit as st
from database.queries.stats_history import get_all_statistiques, get_statistique_by_year
import matplotlib.pyplot as plt


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
    st.title("Statistiques")
    unique_years = sorted(list(set(s.year for s in get_all_statistiques())))
    year_to_display = st.selectbox("Choisir une année", options=unique_years)
    display_charts_for_year(year_to_display)


main()
