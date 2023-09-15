import pandas as pd
import streamlit as st
import plotly.express as px

from database.queries.adherents import (get_student_ratio, get_gender_ratio, get_job_seeker_ratio,
                                        get_cefim_alumni_ratio, get_cefim_instructor_ratio, get_adult_ratio,
                                        get_child_ratio, get_adherents_by_year, get_revenue)
from database.queries.stats_history import get_all_statistiques
from utils.helpers import ACTUAL_YEAR


def display_gender_ratio():
    males, females = get_gender_ratio()
    labels = ['Hommes', 'Femmes']
    values = [males, females]
    fig = px.pie(names=labels, values=values, title="Répartition par genre")
    st.plotly_chart(fig)


def display_status_ratio():
    labels = [
        'Étudiants',
        'Demandeurs d\'emploi',
        'Anciens étudiants de CEFIM',
        'Formateurs à CEFIM',
        'Adultes',
        'Enfants',
    ]
    values = [
        get_student_ratio(),
        get_job_seeker_ratio(),
        get_cefim_alumni_ratio(),
        get_cefim_instructor_ratio(),
        get_adult_ratio(),
        get_child_ratio(),
    ]
    fig = px.pie(names=labels, values=values, title="Répartition par statut")
    st.plotly_chart(fig)


def display_revenue_evolution():
    historical_stats = get_all_statistiques()
    df = pd.DataFrame([
        {
            "Année": stat.year,
            "Chiffre d'affaires": stat.revenue,
            "Légende": "Évolution du chiffre d'affaire"
        }
        for stat in historical_stats
    ])

    total_cotisations_actual = get_revenue()

    fig = px.line(df, x="Année", y="Chiffre d'affaires", title="Évolution du Chiffre d'Affaires au fil des années", color="Légende")

    # Ajoutez une barre pour le chiffre d'affaires de 2023
    fig.add_bar(x=[ACTUAL_YEAR], y=[total_cotisations_actual], name=f'Chiffre d\'affaires en {ACTUAL_YEAR}', marker_color='red')

    # Ajoutez une annotation pour la valeur au-dessus de la barre
    fig.add_annotation(
        x=ACTUAL_YEAR,
        y=total_cotisations_actual,
        text=f"{total_cotisations_actual} €",
        showarrow=False,
        yshift=10
    )

    st.plotly_chart(fig)
    st.write(f"Total des cotisations des adhérents en {ACTUAL_YEAR} : {total_cotisations_actual} €")


if __name__ == "__main__":
    st.title(f"Statistiques {ACTUAL_YEAR}")

    tabs = st.tabs(["Répartition des genres", "Répartitions des statuts", "Chiffre d'affaire en cours"])

    with tabs[0]:
        display_gender_ratio()

    with tabs[1]:
        display_status_ratio()

    with tabs[2]:
        display_revenue_evolution()
