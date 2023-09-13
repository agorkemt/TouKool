import datetime
from sqlalchemy import Enum

LAST_YEAR = datetime.datetime.now().year-1
ACTUAL_YEAR = datetime.datetime.now().year


class StatutEnum(Enum):
    ADULTE = ("Adulte", 20.0)
    ENFANT = ("Enfant", 10.0)
    ETUDIANT = ("Étudiant", 5.0)
    DEMANDEUR_EMPLOI = ("Demandeur d'emploi", 8.0)
    ANCIEN_ETUDIANT_CEFIM = ("Ancien étudiant de CEFIM", 9.0)
    FORMATEUR_CEFIM = ("Formateur à CEFIM", 0.0)
