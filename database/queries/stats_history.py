from database.session import SessionLocal
from database.models import StatistiqueHistorique
import streamlit as st


def insert_statistique(stat):
    db = SessionLocal()
    try:
        db.add(stat)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_statistique_by_year(year):
    db = SessionLocal()
    try:
        return db.query(StatistiqueHistorique).filter_by(year=year).first()
    except Exception as e:
        st.error(f"Error fetching statistics: {e}")
    finally:
        db.close()


def get_all_statistiques():
    db = SessionLocal()
    try:
        return db.query(StatistiqueHistorique).all()
    finally:
        db.close()
