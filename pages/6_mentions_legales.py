import streamlit as st

def display_legal_mentions():
    st.title("Mentions Légales du site TouKoul")

    st.subheader("Identification du professionnel")
    st.write("""
    - **Nom de l'entreprise** : TouKoul Paddle Club
    - **Forme juridique** : Association loi 1901
    - **Adresse** : 123 Quai des Paddleurs, 75000 Paris
    - **Numéro d'immatriculation** : RCS Paris 123 456 789
    - **Numéro d'identification à la TVA** : FR 12 345 678 901
    - **Email** : contact@toukoulpaddleclub.fr
    - **Numéro de téléphone** : 01 23 45 67 89
    """)

    st.subheader("Hébergeur du site")
    st.write("""
    - **Nom** : WebHostPro
    - **Adresse** : 456 rue des Serveurs, 69000 Lyon
    - **Numéro de téléphone** : 04 56 78 90 12
    """)

    st.subheader("Conditions générales de vente (CGV)")
    st.write("Les conditions générales de vente sont disponibles sur une page dédiée. Elles détaillent les modalités d'inscription, les tarifs des différentes offres, les conditions de résiliation, etc.")

    st.subheader("Traitement des données personnelles et utilisation de cookies")
    st.write("""
    - **Responsable du traitement** : M. Jean Dupont, président de TouKoul Paddle Club.
    - **Finalité** : Les données sont collectées pour gérer les inscriptions, informer les membres des événements à venir, et améliorer l'expérience utilisateur sur le site.
    - **Droits** : Conformément à la réglementation en vigueur, vous disposez d'un droit d'accès, de rectification, de suppression et d'opposition de vos données. Pour cela, contactez-nous à l'adresse email mentionnée ci-dessus.
    - **Cookies** : Notre site utilise des cookies pour améliorer l'expérience utilisateur et analyser le trafic. Vous avez la possibilité de refuser ces cookies via les paramètres de votre navigateur.
    """)

    st.subheader("Résiliation d'abonnement par voie électronique")
    st.write("""
    Si vous souhaitez résilier votre adhésion au club TouKoul, une fonctionnalité est mise à votre disposition dans votre espace membre. Suivez les instructions pour procéder à la résiliation.
    """)

    st.subheader("Mentions obligatoires pour la fonctionnalité de résiliation")
    st.write("""
    La fonctionnalité de résiliation est clairement identifiée sous la mention "Résilier mon adhésion". Elle vous fournira toutes les informations nécessaires pour finaliser votre résiliation.
    """)

if __name__ == "__main__":
    display_legal_mentions()