import pandas as pd
import streamlit as st
from database.queries.stats_history import get_all_statistiques, get_statistique_by_year
import plotly.express as px

st.set_page_config(
    page_title="Historiques",
    layout="wide"
)
historical_stats = get_all_statistiques()

# Define your data here (replace with your actual data)
df = pd.DataFrame([
    {
        "Année": stat.year,
        "Hommes": stat.male_ratio * 100,
        "Femmes": stat.female_ratio * 100,
        "Étudiant": stat.ratio_etudiant * 100,
        "Demandeur d'emploi": stat.ratio_demandeur_emploi * 100,
        "Ancien étudiant CEFIM": stat.ratio_ancien_etudiant_cefim * 100,
        "Formateur CEFIM": stat.ratio_formateur_cefim * 100,
        "Famille": stat.ratio_famille * 100,
        "Enfant": stat.ratio_enfant * 100,
        "Adulte": stat.ratio_adulte * 100,
        "Chiffre d'affaires": stat.revenue
    }
    for stat in historical_stats
])

# Create Plotly figures
fig1 = px.line(df, x="Année", y=["Hommes", "Femmes"], title="Évolution du Ratio Hommes/Femmes au fil des années")
fig2 = px.line(df, x="Année", y=["Étudiant", "Demandeur d'emploi", "Ancien étudiant CEFIM", "Formateur CEFIM", "Famille"],
               title="Évolution des Ratios par Statut au fil des années")
fig3 = px.line(df, x="Année", y=["Enfant", "Adulte"], title="Évolution du Ratio Enfant/Adulte au fil des années")
fig4 = px.line(df, x="Année", y="Chiffre d'affaires", title="Évolution du Chiffre d'Affaires au fil des années")


if __name__ == "__main__":
    tabs = st.tabs(
        ["Nombre d'adhérents", "Évolutions", "Chiffre d'affaire"]
    )
    with tabs[0]:
        st.plotly_chart(fig3)

    with tabs[1]:
        col1, col2= st.columns(2)

        with col1:
            st.plotly_chart(fig1)

        with col2:
            st.plotly_chart(fig2)

    with tabs[2]:
        st.plotly_chart(fig4)

