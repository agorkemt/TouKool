from sqlalchemy import Column, Integer, String, Boolean, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Adherent(Base):
    __tablename__ = "adherents"

    id = Column(Integer, primary_key=True, index=True, comment="Identifiant unique pour chaque adhérent")
    nom = Column(String, nullable=False, comment="Nom de l'adhérent")
    prenom = Column(String, nullable=False, comment="Prénom de l'adhérent")
    adresse_postale = Column(String, nullable=False, comment="Adresse postale de l'adhérent")
    email = Column(String, unique=True, index=True, nullable=False, comment="Adresse e-mail de l'adhérent")
    genre = Column(String, nullable=False, comment="Genre de l'adhérent")
    annee_adhesion = Column(Integer, nullable=False, comment="Année d'adhésion de l'adhérent")
    certificat_medical = Column(Boolean, default=False, comment="Statut du certificat médical de l'adhérent")
    cotisation_payee = Column(Boolean, default=False, comment="Statut de paiement de la cotisation de l'adhérent")
    date_naissance = Column(Date, nullable=False, comment="Date de naissance de l'adhérent")
    latitude = Column(Float, comment="Latitude de l'adresse de l'adhérent")
    longitude = Column(Float, comment="Longitude de l'adresse de l'adhérent")
    statut = Column(String, nullable=False,
                    comment="Statut de l'adhérent (Adulte,Enfant,Étudiant, Demandeur d'emploi, Ancien étudiant de "
                            "CEFIM, Formateur à CEFIM)")
    cotisation = Column(Float, nullable=False, comment="Montant de la cotisation de l'adhérent")


class StatistiqueHistorique(Base):
    __tablename__ = 'stats_history'

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    adherent_count = Column(Integer, nullable=False)
    male_ratio = Column(Float, nullable=False)
    female_ratio = Column(Float, nullable=False)
    ratio_etudiant = Column(Float, nullable=False)
    ratio_demandeur_emploi = Column(Float, nullable=False)
    ratio_ancien_etudiant_cefim = Column(Float, nullable=False)
    ratio_formateur_cefim = Column(Float, nullable=False)
    ratio_famille = Column(Float, nullable=False)
    ratio_enfant = Column(Float, nullable=False)
    ratio_adulte = Column(Float, nullable=False)
    revenue = Column(Float, nullable=False)

