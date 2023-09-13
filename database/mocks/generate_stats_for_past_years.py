from datetime import datetime
from database.models import StatistiqueHistorique
from database.session import SessionLocal
import random


def generate_stats_for_past_years():
    db = SessionLocal()

    # Valeurs initiales
    initial_adherents = 100
    growth_rate = 1.3

    # Pour les cinq dernières années
    current_year = datetime.now().year
    for year in range(current_year - 5, current_year):
        adherents = int(initial_adherents * (growth_rate ** (year - (current_year - 5))))

        # Simuler des variations pour les ratios
        male_ratio = 0.5 + random.uniform(-0.05, 0.05)
        female_ratio = 1 - male_ratio

        # Simuler des ratios pour les statuts avec une variation aléatoire
        ratios = {
            'ratio_etudiant': 0.2 + random.uniform(-0.05, 0.05),
            'ratio_demandeur_emploi': 0.1 + random.uniform(-0.02, 0.02),
            'ratio_ancien_etudiant_cefim': 0.15 + random.uniform(-0.03, 0.03),
            'ratio_formateur_cefim': 0.05 + random.uniform(-0.01, 0.01),
            'ratio_enfant': 0.15 + random.uniform(-0.03, 0.03)
        }

        # Ajuster les ratios pour qu'ils somment à 1
        total_ratio = sum(ratios.values())
        for key in ratios:
            ratios[key] = ratios[key] / total_ratio

        ratio_adulte = 1 - ratios['ratio_enfant']

        # Générer un ratio pour la famille qui est indépendant
        ratio_famille = 0.3 + random.uniform(-0.05, 0.05)

        # Créer un nouvel enregistrement de statistiques
        stats = StatistiqueHistorique(
            year=year,
            adherent_count=adherents,
            male_ratio=male_ratio,
            female_ratio=female_ratio,
            ratio_etudiant=ratios['ratio_etudiant'],
            ratio_demandeur_emploi=ratios['ratio_demandeur_emploi'],
            ratio_ancien_etudiant_cefim=ratios['ratio_ancien_etudiant_cefim'],
            ratio_formateur_cefim=ratios['ratio_formateur_cefim'],
            ratio_famille=ratio_famille,
            ratio_enfant=ratios['ratio_enfant'],
            ratio_adulte=ratio_adulte
        )

        db.add(stats)
        db.commit()

    db.close()


generate_stats_for_past_years()
