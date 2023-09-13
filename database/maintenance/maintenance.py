import sqlite3
from datetime import datetime
from database.models import StatistiqueHistorique
from database.queries.adherents import (get_gender_ratio, get_number_adherents, get_job_seeker_ratio,
                                        get_cefim_alumni_ratio,
                                        get_cefim_instructor_ratio, get_family_ratio, get_student_ratio,
                                        get_adult_ratio, get_child_ratio)
from database.session import SessionLocal
from utils.helpers import LAST_YEAR


def supprimer_adherents_annee_precedente():
    conn = sqlite3.connect('adherents.db')
    cursor = conn.cursor()

    delete_query = """
        DELETE FROM adherents
        WHERE 
            annee_adhesion = strftime('%Y', 'now', '-1 year')
            AND id NOT IN (
                SELECT id FROM adherents
                WHERE annee_adhesion = strftime('%Y', 'now')
            );
    """

    cursor.execute(delete_query)
    conn.commit()
    conn.close()


def check_and_delete_old_adherents():
    current_date = datetime.now()
    if current_date.month == 10 and current_date.day == 1:
        supprimer_adherents_annee_precedente()


def record_yearly_statistics():
    db = SessionLocal()

    year = LAST_YEAR
    adherent_count = get_number_adherents()
    male_ratio, female_ratio = get_gender_ratio()

    stats = StatistiqueHistorique(
        year=year,
        adherent_count=adherent_count,
        male_ratio=male_ratio,
        female_ratio=female_ratio,
        ratio_etudiant=get_student_ratio(),
        ratio_demandeur_emploi=get_job_seeker_ratio(),
        ratio_ancien_etudiant_cefim=get_cefim_alumni_ratio(),
        ratio_formateur_cefim=get_cefim_instructor_ratio(),
        ratio_famille=get_family_ratio(),
        ratio_enfant=get_child_ratio(),
        ratio_adulte=get_adult_ratio()
    )

    db.add(stats)
    db.commit()
    db.close()


def check_and_record_statistics():
    current_date = datetime.now()
    if current_date.month == 9 and current_date.day == 1:
        record_yearly_statistics()
