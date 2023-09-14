import pandas as pd
import streamlit as st
from collections import defaultdict
from database.queries.adherents import calculate_age, get_all_adherents, get_number_adherents
import matplotlib.pyplot as plt
import plotly.express as px

from database.queries.stats_history import get_all_statistiques

st.set_page_config(
    page_title="Statistiques",
    layout="wide"
)


def age_distribution(adherents):
    ages = [calculate_age(adherent.date_naissance) for adherent in adherents]
    return {age: ages.count(age) for age in set(ages)}


def family_analysis():
    try:
        families = defaultdict(list)
        adherentsAll = get_all_adherents()
        for adherent in adherentsAll:
            families[adherent.nom].append(adherent)

        avg_children = sum(1 for members in families.values() if
                           any(calculate_age(member.date_naissance) <= 18 for member in members)) / len(families)
        avg_adults = sum(1 for members in families.values() if
                         any(calculate_age(member.date_naissance) > 18 for member in members)) / len(families)

        return {
            "average_children_per_family": avg_children,
            "average_adults_per_family": avg_adults
        }
    except Exception as e:
        print(f"Error fetching family analysis: {e}")
        return {}


def display_age_distribution():
    data = age_distribution(get_all_adherents())
    fig, ax = plt.subplots()
    ax.bar(data.keys(), data.values(), color='skyblue')
    ax.set_title('Répartition par âge des adhérents')
    ax.set_xlabel('Âge')
    ax.set_ylabel('Nombre d\'adhérents')
    st.pyplot(fig)


def age_category_distribution():
    adherentsAll = get_all_adherents()
    categories = {
        "Enfants": (6, 12),
        "Adolescents": (13, 18),
        "Jeunes adultes": (19, 30),
        "Adultes": (31, 50),
        "Seniors": (51, 70)
    }
    distribution = defaultdict(int)

    for adherent in adherentsAll:
        age = calculate_age(adherent.date_naissance)
        for category, (min_age, max_age) in categories.items():
            if min_age <= age <= max_age:
                distribution[category] += 1
                break

    return distribution


def display_age_category_distribution():
    data = age_category_distribution()
    categories_order = [
        "Enfants",
        "Adolescents",
        "Jeunes adultes",
        "Adultes",
        "Seniors"
    ]
    age_ranges = {
        "Enfants": "6-12 ans",
        "Adolescents": "13-18 ans",
        "Jeunes adultes": "19-30 ans",
        "Adultes": "31-50 ans",
        "Seniors": "51-70 ans"
    }

    # Organiser les données dans le bon ordre
    ordered_data = [data[cat] for cat in categories_order]

    fig, ax = plt.subplots()
    bars = ax.bar(categories_order, ordered_data, color='lightgreen')

    # Remplacer les étiquettes de l'axe des abscisses par les plages d'âge
    ax.set_xticklabels([age_ranges[cat] for cat in categories_order])

    ax.set_title('Répartition par catégorie d\'âge des adhérents')
    ax.set_xlabel('Catégorie d\'âge')
    ax.set_ylabel('Nombre d\'adhérents')
    st.pyplot(fig)


def display_family_analysis():
    data = family_analysis()
    fig, ax = plt.subplots()
    categories = ['Enfants par famille', 'Adultes par famille']
    ax.bar(categories, [data['average_children_per_family'], data['average_adults_per_family']],
           color=['pink', 'purple'])
    ax.set_title('Analyse moyenne des membres par famille')
    ax.set_ylabel('Moyenne')
    st.pyplot(fig)


def display_revenue_over_time():
    # Récupérez les données de chiffre d'affaires à partir de la base de données
    stats = get_all_statistiques()

    # Créez un DataFrame pandas à partir des données
    data = {
        "Année": [stat.year for stat in stats],
        "Chiffre d'affaires": [stat.revenue for stat in stats]
    }

    df = pd.DataFrame(data)

    # Créez un graphique linéaire avec Plotly Express
    fig = px.line(df, x="Année", y="Chiffre d'affaires", title="Évolution du chiffre d'affaires au fil des années")

    # Affichez le graphique dans Streamlit
    st.plotly_chart(fig)


if __name__ == "__main__":
    tabs = st.tabs(
        ["Statistiques sur l'âge", "Nombre d'adhérents", "Chiffre d'affaire"]
    )

    # Onglet pour les statistiques sur l'âge
    with tabs[0]:
        col1, col2, col3 = st.columns(3)

        with col1:
            display_age_distribution()

        with col2:
            display_age_category_distribution()

        with col3:
            display_family_analysis()

    # Onglet pour le nombre d'adhérents
    with tabs[1]:
        st.write("Nombre d'adhérents : ", get_number_adherents())

    # Onglet pour le chiffre d'affaire
    with tabs[2]:
        # Supposons que vous ayez une fonction get_revenue()
        display_revenue_over_time()
