
from faker import Faker
from fhir.resources.observation import Observation
from fhir.resources.patient import Patient
import json
from datetime import datetime, timedelta
from confluent_kafka import Consumer, Producer
from elasticsearch import Elasticsearch
import random
import os 
import pytz

from product import produce_to_kafka


# J'ai crée une fonction pour pouvoir simuler n observation de pression artérielle

file_path = "dernière_date.txt"


# Charger la dernière date sauvegardée
if os.path.exists(file_path):
    with open(file_path, "r") as file:
        last_date_str = file.read().strip()
        # Essayer de lire au format avec fuseau horaire
        try:
            # Utiliser %z pour inclure le fuseau horaire
            current_date = datetime.strptime(last_date_str, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            # Si le format avec fuseau horaire échoue, essayer sans fuseau horaire
            try:
                current_date = datetime.strptime(last_date_str, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                # Si la date n'a pas l'heure, tenter de la lire au format date seulement
                current_date = datetime.strptime(last_date_str, "%Y-%m-%d")
                current_date = current_date.replace(hour=0, minute=0, second=0)  # Ajouter 00:00:00
else:
    current_date = datetime(2020, 1, 1, 0, 0)  # Date par défaut avec heure à 00:00

# J'ai appliquer ici un fuseau horaire UTC 
# J'ai appliquer ici un fuseau horaire UTC 
utc_zone = pytz.utc
if current_date.tzinfo is None:
    current_date = utc_zone.localize(current_date)


fake = Faker()

liste_id = []
patient_name_liste = []
sex_liste = []

# Création du dictionnaire vide en dehors de la boucle
dict_name_id = {}
for i in range(100):
    # Générer un ID unique
    patient_id = fake.uuid4()
    liste_id.append(patient_id)

    # Générer des noms homme et femme
    patient_name_homme = fake.name_male()
    patient_name_femme = fake.name_female()

    # Choisir aléatoirement un nom parmi les deux
    patient_names = random.choice([patient_name_homme, patient_name_femme])

    # Déterminer le sexe en fonction du choix
    if patient_names == patient_name_homme:
        sexe = "Homme"
    else:
        sexe = "Femme"

    # Ajouter le sexe et le nom à leurs listes respectives
    sex_liste.append(sexe)
    patient_name_liste.append(patient_names)

# Utilisation de zip() pour associer ID, prénom et sexe
dict_name_id = dict(zip(liste_id, zip(patient_name_liste, sex_liste)))



for i in range (500):
# Fonction pour générer une observation de pression artérielle
        def generate_blood_pressure_observation(patient_id, systolic, diastolic, random_date_str, patient_name):
            # Créer une observation FHIR
            observation = {
                "id": patient_id,
                "status": "final",
                "category": [{
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "vital-signs",
                        "display": "Vital Signs"
                    }]
                }],
                "code": {
                    "coding": [{
                        "system": "http://loinc.org",
                        "code": "85354-9",
                        "display": "Blood pressure"
                    }]
                },
                "subject": {
                    "reference": f"Patient/{patient_id}",
                    "display": patient_name
                },
                "effectiveDateTime": random_date_str,  # Date avec fuseau horaire
                "component": [
                    {
                        "code": {
                            "coding": [{
                                "system": "http://loinc.org",
                                "code": "8480-6",
                                "display": "Systolic Blood Pressure"
                            }]
                        },
                        "valueQuantity": {
                            "value": systolic,
                            "unit": "mmHg",
                            "system": "http://unitsofmeasure.org",
                            "code": "mm[Hg]"
                        }
                    },
                    {
                        "code": {
                            "coding": [{
                                "system": "http://loinc.org",
                                "code": "8462-4",
                                "display": "Diastolic Blood Pressure"
                            }]
                        },
                        "valueQuantity": {
                            "value": diastolic,
                            "unit": "mmHg",
                            "system": "http://unitsofmeasure.org",
                            "code": "mm[Hg]"
                        }
                    }
                ]
            }

            return observation

        fake = Faker()
        # Générer les données aléatoires pour chaque observation
        systolic = fake.random_int(min=78, max=190)  # Pression systolique
        diastolic = fake.random_int(min=40, max=130)  # Pression diastolique

        # je génére ici une date aléatoire pour la variable date
        delta_days = random.randint(0, 3)
        delta_hours = random.randint(0, 23)
        delta_minutes = random.randint(0, 59)
        delta_seconds = random.randint(0, 59)
        delta = timedelta(days=delta_days, hours=delta_hours, minutes=delta_minutes, seconds=delta_seconds)

        # pour chosir un ID aléatoire

        patient_id = random.choice(list(dict_name_id.keys()))  
        patient_name, sexe = dict_name_id[patient_id]


        # Mettre à jour la date actuelle
        current_date += delta

        # Convertir la date en chaîne au format ISO 8601 avec fuseau horaire UTC
        random_date_str = current_date.strftime("%Y-%m-%dT%H:%M:%S%z")

        # Générer l'observation
        observation = generate_blood_pressure_observation(patient_id, systolic, diastolic, random_date_str, patient_name)
        print(observation)

    # Sauvegarder la dernière date dans le fichier
        with open(file_path, "w") as file:
            file.write(current_date.strftime("%Y-%m-%dT%H:%M:%S%z"))


        # generation du message dans observation

        observations = generate_blood_pressure_observation(patient_id, systolic, diastolic, random_date_str, patient_name)


        print(f"Observation générée pour le patient {patient_id}")


        # Envoyer les messages vers notre topics Kafka

        produce_to_kafka(observations)
   
