from sqlalchemy import func, select, and_
import streamlit as st

from utils.helpers import ACTUAL_YEAR
from database.session import SessionLocal
from database.models import Adherent
from sqlalchemy.exc import IntegrityError


def get_all_adherents():
    db = SessionLocal()
    adherents = db.query(Adherent).all()
    db.close()
    return adherents


def get_number_adherents():
    db = SessionLocal()
    try:
        count = db.execute(select(func.count(Adherent.id)).where(Adherent.annee_adhesion == ACTUAL_YEAR)).scalar_one()
        return count
    except Exception as e:
        st.error(f"Error fetching adherent count: {e}")
    finally:
        db.close()


def add_adherent(adherent_data):
    db = SessionLocal()
    try:
        adherent = Adherent(**adherent_data)
        db.add(adherent)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_adherents(search=None):
    session = SessionLocal()
    try:
        query = session.query(Adherent)
        if search:
            query = query.filter(Adherent.nom.like(f"%{search}%"))
        return query.all()
    finally:
        session.close()


def modify_adherent(adherent_data, adherent_id):
    session = SessionLocal()
    try:
        adherent = session.query(Adherent).filter(Adherent.id == adherent_id).one()

        for key, value in adherent_data.items():
            setattr(adherent, key, value)

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_adherents_by_year(year):
    session = SessionLocal()
    try:
        return session.query(Adherent).filter(Adherent.annee_adhesion == year).all()
    finally:
        session.close()


def get_gender_ratio():
    db = SessionLocal()
    total = db.query(Adherent).count()
    males = db.query(Adherent).filter(Adherent.genre == 'Homme').count()
    females = total - males
    db.close()
    return males / total, females / total


def get_student_ratio():
    db = SessionLocal()
    total = db.query(Adherent).count()
    students = db.query(Adherent).filter(Adherent.statut == 'Étudiant').count()
    db.close()
    return students / total


def get_job_seeker_ratio():
    db = SessionLocal()
    total = db.query(Adherent).count()
    job_seekers = db.query(Adherent).filter(Adherent.statut == "Demandeur d'emploi").count()
    db.close()
    return job_seekers / total


def get_cefim_alumni_ratio():
    db = SessionLocal()
    total = db.query(Adherent).count()
    cefim_alumni = db.query(Adherent).filter(Adherent.statut == "Ancien étudiant de CEFIM").count()
    db.close()
    return cefim_alumni / total


def get_cefim_instructor_ratio():
    db = SessionLocal()
    total = db.query(Adherent).count()
    cefim_instructors = db.query(Adherent).filter(Adherent.statut == "Formateur à CEFIM").count()
    db.close()
    return cefim_instructors / total


def get_family_member_count():
    db = SessionLocal()

    families = db.query(Adherent.nom, Adherent.adresse_postale).group_by(Adherent.nom, Adherent.adresse_postale).having(
        func.count(Adherent.id) > 1).all()

    family_member_count = 0
    for family in families:
        family_member_count += db.query(Adherent).filter(
            and_(Adherent.nom == family.nom, Adherent.adresse_postale == family.adresse_postale)).count()

    db.close()
    return family_member_count


def get_family_ratio():
    db = SessionLocal()
    total = db.query(Adherent).count()
    family_member_count = get_family_member_count()
    db.close()
    return family_member_count / total


def get_adult_ratio():
    db = SessionLocal()
    total = db.query(Adherent).count()
    adults = db.query(Adherent).filter(Adherent.statut == "Adulte").count()
    db.close()
    return adults / total


def get_child_ratio():
    db = SessionLocal()
    total = db.query(Adherent).count()
    children = db.query(Adherent).filter(Adherent.statut == "Enfant").count()
    db.close()
    return children / total
