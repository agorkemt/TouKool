import streamlit as st
from sqlalchemy.exc import IntegrityError
import pandas as pd
import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
from database.queries import adherents
from utils.geocoding import get_lat_lng_from_address

LAST_YEAR = datetime.datetime.now().year - 1
FIELDS = ["nom", "prenom", "adresse_postale", "ville", "code_postal", "email", "genre_index", "annee_adhesion",
          "certificat_medical", "cotisation_payee", "selection_made"]


def clear_form():
    for field in FIELDS:
        if field in st.session_state:
            del st.session_state[field]


def get_full_address(adresse_postale, ville, code_postal):
    return "{}, {}, {}".format(adresse_postale, ville, code_postal)


def submit_form():
    nom = st.session_state.get("nom", "")
    prenom = st.session_state.get("prenom", "")
    date_naissance = st.session_state.get("date_naissance", datetime.date.today())
    adresse_postale = st.session_state.get("adresse_postale", "")
    ville = st.session_state.get("ville", "")
    code_postal = st.session_state.get("code_postal", "")
    email = st.session_state.get("email", "")
    genre = st.session_state.get("genre", "Homme")
    annee_adhesion = st.session_state.get("annee_adhesion", LAST_YEAR)
    certificat_medical = st.session_state.get("certificat_medical", False)
    cotisation_payee = st.session_state.get("cotisation_payee", False)
    is_selection_made = st.session_state.get("selection_made", False)

    if not nom:
        st.warning("Le nom est requis.")
    if not prenom:
        st.warning("Le prénom est requis.")
    if not adresse_postale:
        st.warning("L'adresse postale est requise.")
    if not ville:
        st.warning("La ville est requise.")
    if not code_postal:
        st.warning("Le code postal est requis.")
    if not email:
        st.warning("L'email est requis.")
    elif "@" not in email:
        st.warning("L'email n'est pas valide.")

    if all([nom, prenom, adresse_postale, ville, code_postal, email]):
        full_address = get_full_address(adresse_postale, ville, code_postal)
        latitude, longitude = get_lat_lng_from_address(full_address)
        if st.session_state.statut == "Étudiant":
            cotisation = 5
        elif st.session_state.statut == "Demandeur d'emploi":
            cotisation = 8
        elif st.session_state.statut == "Adulte":
            cotisation = 20
        elif st.session_state.statut == "Enfant":
            cotisation = 10
        elif st.session_state.statut == "Ancien étudiant de CEFIM":
            cotisation = 9
        else:
            cotisation = 0.0

        adherent_data = {
            "nom": nom,
            "prenom": prenom,
            "date_naissance": date_naissance,
            "adresse_postale": full_address,
            "email": email,
            "genre": genre,
            "annee_adhesion": annee_adhesion,
            "certificat_medical": certificat_medical,
            "cotisation_payee": cotisation_payee,
            "statut": st.session_state.statut,
            "cotisation": cotisation,
        }
        if latitude and longitude:
            adherent_data["latitude"] = latitude
            adherent_data["longitude"] = longitude
        else:
            st.warning("Impossible de géocoder l'adresse fournie. Veuillez vérifier l'exactitude de l'adresse.")

        if is_selection_made:
            try:
                adherents.modify_adherent(adherent_data, st.session_state.selected_adherent_id)
                st.success("L'adhérent a été modifié avec succès!")
            except Exception as e:
                st.error(f"Une erreur inattendue s'est produite lors de la modification: {e}")
        else:
            try:
                adherents.add_adherent(adherent_data)
                st.success("L'adhérent a été ajouté avec succès!")
            except IntegrityError:
                st.error("Erreur: Une valeur saisie est déjà présente (probablement l'email).")
            except Exception as e:
                st.error(f"Une erreur inattendue s'est produite lors de l'ajout: {e}")
    else:
        st.error("Veuillez remplir tous les champs requis.")


def display_adherents():
    st.write(f"Liste des adhérents encore sous l'année {LAST_YEAR}")
    search_text = st.text_input("Rechercher un adhérent par nom et/ou prénom", key="search_text")
    if st.button("Rafraîchir"):
        st.session_state.refresh_table = not st.session_state.get("refresh_table", False)
    addAdherents = adherents.get_adherents_by_year(LAST_YEAR)
    adherents_data = [{
        "id": adherent.id,
        "nom": adherent.nom,
        "prenom": adherent.prenom,
        "adresse_postale": adherent.adresse_postale,
        "email": adherent.email,
        "genre": adherent.genre,
        "annee_adhesion": adherent.annee_adhesion,
        "certificat_medical": adherent.certificat_medical,
        "cotisation_payee": adherent.cotisation_payee,
    } for adherent in addAdherents]

    if search_text:
        adherents_data = [adherent for adherent in adherents_data if
                          search_text.lower() in adherent["nom"].lower() or search_text.lower() in adherent[
                              "prenom"].lower()]

    if adherents:
        df = pd.DataFrame(adherents_data)

        builder = GridOptionsBuilder.from_dataframe(df, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)
        builder.configure_selection(selection_mode='single', use_checkbox=True)
        builder.configure_pagination(paginationPageSize=24, paginationAutoPageSize=False, enabled=True)
        builder.configure_default_column(sorteable=True, filterable=True, filter=True)
        grid_options = builder.build()
        grid_options['enableCellSelection'] = False
        grid_options['columnDefs'][0]['checkboxSelection'] = True
        grid_options['defaultColDef'] = {
            'width': 150,
            'resizable': True
        }
        return_value = AgGrid(df, gridOptions=grid_options)
        st.button('Charger données')

        if 'selected_rows' in return_value and return_value['selected_rows']:
            selected_row = return_value['selected_rows'][0]

            adresse_parts = selected_row["adresse_postale"].split(", ")

            adresse = adresse_parts[0]
            ville = adresse_parts[1]
            code_postal = adresse_parts[2]

            st.session_state.selection_made = True
            st.session_state.selected_adherent_id = selected_row["id"]
            st.session_state.nom = selected_row["nom"]
            st.session_state.prenom = selected_row["prenom"]
            st.session_state.adresse_postale = adresse
            st.session_state.ville = ville
            st.session_state.code_postal = code_postal
            st.session_state.email = selected_row["email"]
            st.session_state.genre = selected_row["genre"]
            st.session_state.annee_adhesion = selected_row["annee_adhesion"]
            st.session_state.certificat_medical = selected_row["certificat_medical"]
            st.session_state.cotisation_payee = selected_row["cotisation_payee"]

            if not st.session_state.get('delete_success', False):
                if st.button("Supprimer"):
                    st.session_state.delete_clicked = True

                if st.session_state.get('delete_clicked'):
                    if st.checkbox("Êtes-vous sûr de vouloir supprimer cet adhérent ?"):
                        st.write(f"ID de l'adhérent sélectionné : {st.session_state.selected_adherent_id}")
                        try:
                            adherents.delete_adherent(st.session_state.selected_adherent_id)
                            st.success("L'adhérent a été supprimé avec succès!")
                            st.session_state.selected_adherent_id = None
                            st.session_state.delete_clicked = False
                            st.session_state.delete_success = True
                        except Exception as e:
                            st.error(f"Une erreur s'est produite lors de la suppression: {e}")
            else:
                st.session_state.selection_made = False
                st.session_state.delete_success = False


def display_form():
    st.write("Formulaire d'adhésion")
    st.session_state.nom = st.text_input("Nom", value=st.session_state.get("nom", ""))
    st.session_state.prenom = st.text_input("Prénom", value=st.session_state.get("prenom", ""))
    st.session_state.date_naissance = st.date_input("Date de naissance",
                                                    value=st.session_state.get("date_naissance", datetime.date.today()))
    st.session_state.adresse_postale = st.text_input("Adresse postale",
                                                     value=st.session_state.get("adresse_postale", ""))
    st.session_state.ville = st.text_input("Ville", value=st.session_state.get("ville", ""))
    st.session_state.code_postal = st.text_input("Code postal", value=st.session_state.get("code_postal", ""))
    st.session_state.email = st.text_input("Email", value=st.session_state.get("email", ""))
    st.session_state.genre = st.selectbox("Genre", ["Homme", "Femme"], index=st.session_state.get("genre_index", 0))
    statuts_adhesion = ["Adulte", "Enfant", "Étudiant", "Demandeur d'emploi", "Ancien étudiant de CEFIM",
                        "Formateur à CEFIM"]

    selected_statut_index = statuts_adhesion.index(st.session_state.get("statut", "Adulte"))

    selected_statut = st.selectbox("Statut d'adhésion", statuts_adhesion, index=selected_statut_index)

    st.session_state.statut = selected_statut
    st.session_state.annee_adhesion = st.number_input("Année d'adhésion", min_value=1900, max_value=2100,
                                                      value=st.session_state.get("annee_adhesion", LAST_YEAR))
    st.session_state.certificat_medical = st.checkbox("Certificat médical fourni",
                                                      value=st.session_state.get("certificat_medical", False))
    st.session_state.cotisation_payee = st.checkbox("Cotisation payée",
                                                    value=st.session_state.get("cotisation_payee", False))


def run_gestion_adherent():
    clear_button = st.button("Vider le formulaire")
    if clear_button:
        clear_form()

    col1, col2 = st.columns([2, 3])

    if "selection_made" not in st.session_state:
        st.session_state.selection_made = False

    with col1:
        with st.form(key="adherent_form", clear_on_submit=True):
            display_form()
            if st.session_state.selection_made:
                submit_button = st.form_submit_button("Reinscrire")
            else:
                submit_button = st.form_submit_button("Soumettre")
            if submit_button:
                submit_form()

    with col2:
        display_adherents()
