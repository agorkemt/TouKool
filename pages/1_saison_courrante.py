import streamlit as st
import pandas as pd
import st_aggrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import DataReturnMode, GridUpdateMode
from utils.email_sender import send_email

from database.queries.adherents import get_adherents_by_year, delete_multiple_adherents, get_adherents_without_payment, \
    modify_adherent
from utils.helpers import ACTUAL_YEAR

st.set_page_config(
    page_title=f"Saison {ACTUAL_YEAR}",
    layout="wide"
)


def saison_en_cours():
    st.title(f"Saison {ACTUAL_YEAR}")

    # Récupération des adhérents pour la saison actuelle
    adherents = get_adherents_by_year(ACTUAL_YEAR)
    adherents_with_cotisation_payee = [adherent for adherent in adherents if adherent.cotisation_payee]

    # Conversion des adhérents en DataFrame
    df = pd.DataFrame([adherent.__dict__ for adherent in adherents_with_cotisation_payee])

    # Suppression de la colonne '_sa_instance_state' qui est spécifique à SQLAlchemy et non nécessaire ici
    if '_sa_instance_state' in df.columns:
        df.drop('_sa_instance_state', axis=1, inplace=True)

    df['nom_prenom'] = df['nom'] + " " + df['prenom']

    # Configuration de l'AgGrid avec GridOptionsBuilder
    go = GridOptionsBuilder.from_dataframe(df)
    go.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
    go.configure_pagination(enabled=True, paginationPageSize=24, paginationAutoPageSize=False)
    gridOptions = go.build()
    gridOptions['domLayout'] = 'autoHeight'
    if st.button("Rafraîchir"):
        st.session_state.refresh_table = not st.session_state.get("refresh_table", False)
    # Affichage de l'AgGrid
    response = st_aggrid.AgGrid(
        df,
        gridOptions=gridOptions,
        width='100%',
        data_return_mode=DataReturnMode.AS_INPUT,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
    )

    # Si nécessaire, vous pouvez traiter la réponse pour mettre à jour/supprimer des adhérents
    updated_df = response['data']
    for index, row in updated_df.iterrows():
        original_row = df[df['id'] == row['id']].iloc[0]

        # Comparez chaque colonne pour détecter les modifications
        for column in df.columns:
            if row[column] != original_row[column]:
                # Une modification a été détectée, appelez modify_adherent pour mettre à jour la base de données
                adherent_id = row['id']
                adherent_data = {column: row[column]}
                modify_adherent(adherent_data, adherent_id)

    # Bouton pour supprimer un adhérent
    selected_adherents = st.multiselect("Sélectionnez les adhérents à supprimer", df[['id', 'nom', 'prenom']].apply(
        lambda row: f"{row['id']} - {row['nom']} {row['prenom']}", axis=1))
    selected_ids = [int(adherent.split(' - ')[0]) for adherent in selected_adherents]

    if st.button("Supprimer les adhérents sélectionnés"):
        # Suppression des adhérents sélectionnés
        delete_multiple_adherents(selected_ids)
        st.success(f"{len(selected_ids)} adhérents supprimés avec succès!")
        # Recharger les données pour mettre à jour l'affichage
        adherents = get_adherents_by_year(ACTUAL_YEAR)
        df = pd.DataFrame([adherent.__dict__ for adherent in adherents])

    st.subheader("Adhérents qui n'ont pas encore payé la cotisation")
    unpaid_adherents = get_adherents_without_payment()
    unpaid_df = pd.DataFrame([adherent.__dict__ for adherent in unpaid_adherents])
    if '_sa_instance_state' in unpaid_df.columns:
        unpaid_df.drop('_sa_instance_state', axis=1, inplace=True)

    go_unpaid = GridOptionsBuilder.from_dataframe(unpaid_df)
    go_unpaid.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
    go_unpaid.configure_pagination(enabled=True, paginationPageSize=24, paginationAutoPageSize=False)
    gridOptionsUnpaid = go_unpaid.build()
    gridOptionsUnpaid['domLayout'] = 'autoHeight'

    response_unpaid = st_aggrid.AgGrid(
        unpaid_df,
        gridOptions=gridOptionsUnpaid,
        width='100%',
        data_return_mode=DataReturnMode.AS_INPUT,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
    )

    email_addresses = unpaid_df['email'].tolist()

    # Si l'utilisateur clique sur le bouton, envoyez l'e-mail
    if st.button("Envoyer un rappel par e-mail"):
        subject = "Rappel de paiement de cotisation"
        content = ("Cher adhérent, nous avons remarqué que vous n'avez pas encore payé votre cotisation. Veuillez le "
                   "faire dès que possible. Merci.")
        send_email(subject, content, email_addresses)
        st.success("E-mails envoyés avec succès!")


if __name__ == "__main__":
    saison_en_cours()
