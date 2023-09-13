import threading
import time
from datetime import datetime
from database.maintenance.maintenance import supprimer_adherents_annee_precedente, record_yearly_statistics

# Variable globale pour suivre si le thread a déjà été démarré
THREAD_STARTED = False


def countdown_to_october():
    global THREAD_STARTED

    if not THREAD_STARTED:
        countdown_thread = threading.Thread(target=_countdown_logic, daemon=True)
        countdown_thread.start()
        THREAD_STARTED = True

    current_date = datetime.now()
    october_1st = datetime(current_date.year, 10, 1)

    if current_date > october_1st:
        october_1st = datetime(current_date.year + 1, 10, 1)

    time_difference = october_1st - current_date
    return time_difference.days


def _countdown_logic():
    stats_recorded = False

    while True:
        current_date = datetime.now()
        september_1st = datetime(current_date.year, 9, 1)
        october_1st = datetime(current_date.year, 10, 1)
        time_difference = october_1st - current_date

        if 0 < time_difference.days <= 30 and not stats_recorded:
            record_yearly_statistics()  # La fonction qui enregistre vos statistiques
            stats_recorded = True
            time.sleep(86400)  # Attendre 24 heures avant de vérifier à nouveau

        elif time_difference.total_seconds() <= 0:
            supprimer_adherents_annee_precedente()
            stats_recorded = False  # Réinitialiser pour l'année suivante
            time.sleep(86400)  # Attendre 24 heures avant de vérifier à nouveau

        else:
            time.sleep(3600)  # Attendre 1 heure avant de vérifier à nouveau
