from faker import Faker
from datetime import datetime, timedelta

f = Faker()
start_date = datetime.now()

# Générer une suite de 20 dates croissantes avec isoformat
for _ in range(20):
    # Générer une observation avec une date qui est à la suite de la précédente
    random_date = start_date.isoformat()  # Utilisation de isoformat pour générer la date au format ISO
    print(random_date)

    # Ajouter un nombre de jours (aléatoire entre 1 et 29) à la date précédente pour la prochaine itération
    nb = f.random_int(min=1, max=29)
    h = f.random_int(min=1, max=23)
    start_date += timedelta(days=nb, hours=h)
