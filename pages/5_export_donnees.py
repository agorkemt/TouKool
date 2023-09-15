import streamlit as st
import pandas as pd
import base64
import io
import dicttoxml

from database.queries.adherents import get_all_adherents
from database.queries.stats_history import get_all_statistiques


def sqlalchemy_obj_to_dict(obj):
    """Convertit un objet SQLAlchemy en dictionnaire, en excluant les attributs internes."""
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


def export_data():
    global href
    st.title("Exportation des données")

    # Sélection du modèle à exporter
    model_choice = st.selectbox("Choisissez le modèle à exporter", ["Adherent", "StatistiqueHistorique", "Les deux"])

    # Sélection du format d'exportation
    format_choice = st.selectbox("Choisissez le format d'exportation", ["CSV", "XML"])

    df = None  # Initialisation de df

    if model_choice == "Adherent":
        data = get_all_adherents()
        df = pd.DataFrame([sqlalchemy_obj_to_dict(d) for d in data])
    elif model_choice == "StatistiqueHistorique":
        data = get_all_statistiques()
        df = pd.DataFrame([sqlalchemy_obj_to_dict(d) for d in data])
    elif model_choice == "Les deux":
        data_adherent = get_all_adherents()
        df_adherent = pd.DataFrame([sqlalchemy_obj_to_dict(d) for d in data_adherent])
        data_stat = get_all_statistiques()
        df_stat = pd.DataFrame([sqlalchemy_obj_to_dict(d) for d in data_stat])
        df = pd.concat([df_adherent, df_stat], axis=1)

    if st.button("Exporter les données") and df is not None:
        towrite = io.BytesIO()

        if format_choice == "CSV":
            downloaded_file = df.to_csv(towrite, encoding='utf-8', index=False, sep=";")
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{model_choice}.csv">Télécharger le fichier CSV</a>'
        elif format_choice == "XML":
            xml_data = dicttoxml.dicttoxml(df.to_dict(orient='records'))
            b64 = base64.b64encode(xml_data).decode()
            href = f'<a href="data:file/xml;base64,{b64}" download="{model_choice}.xml">Télécharger le fichier XML</a>'

        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    export_data()
