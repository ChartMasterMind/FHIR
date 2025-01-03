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

# J'ai crée une fonction pour pouvoir simuler n observation de pression artérielle
import os
import random
from datetime import datetime, timedelta
import pytz  # Pour gérer les fuseaux horaires
from faker import Faker

file_path = "dernière_date.txt"

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

# Appliquer le fuseau horaire UTC si nécessaire
utc_zone = pytz.utc
if current_date.tzinfo is None:
    current_date = utc_zone.localize(current_date)

for i in range (50):
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

    # Générer 10 observations
        fake = Faker()
        # Générer les données aléatoires pour chaque observation
        patient_id = fake.uuid4()
        patient_name = fake.name()
        systolic = fake.random_int(min=78, max=190)  # Pression systolique
        diastolic = fake.random_int(min=40, max=130)  # Pression diastolique

        # Générer un delta aléatoire pour la date
        delta_days = random.randint(0, 3)
        delta_hours = random.randint(0, 23)
        delta_minutes = random.randint(0, 59)
        delta_seconds = random.randint(0, 59)
        delta = timedelta(days=delta_days, hours=delta_hours, minutes=delta_minutes, seconds=delta_seconds)

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

         # on créer ici un patient avec un nom généré et aléatoire 
        patient_name_homme = fake.name_male()
        patient_name_femme = fake.name_female()

        patient_name = random.choice([patient_name_homme, patient_name_femme]) 

        # identification du sexe selon le premom pour indexation sur elastic search

        if patient_name == patient_name_homme:
            sexe = "Homme"
        else:
            sexe = "Femme"

        # generation du message dans observation

        observations = generate_blood_pressure_observation(patient_id, systolic, diastolic, random_date_str, patient_name)


        print(f"Observation générée pour le patient {patient_id}")


        # Envoyer les messages vers notre topics Kafka
        def produce_to_kafka(observations):
            producer = Producer({
                'bootstrap.servers': 'localhost:9092',  # Adresse du serveur Kafka
                'group.id': 'python-consumer',
                'auto.offset.reset': 'earliest'
            })

            OBS_JSON = json.dumps(observations)  # Convertir le dict en JSON, nécessaire pour produire avec Kafka
            producer.produce('blood_pressure_topic', value=OBS_JSON)

            print("Observation envoyée à Kafka")
            producer.flush()


        produce_to_kafka(observations)


        # Fonction pour détecter les anomalies
        def detect_anomaly(observations):

            anomaly_type = "tension normale"
    
            if systolic >= 120 and systolic <= 129 and diastolic < 80:
                anomaly_type = "tension élevé"
            
            elif systolic >= 130 and systolic <= 139 and diastolic <= 80 and diastolic <= 89:
                anomaly_type = "Hypertension de stade 1"

            elif systolic > 180 or diastolic > 120:
                anomaly_type = "Crise hypertensive (Urgence immédiate)"

            elif systolic >= 140 or diastolic >= 90:
                anomaly_type = "Hypertension de stade 2"

            elif systolic < 90 or diastolic < 60:
                anomaly_type = "Hypotension"


            print(f"Vérification pour patient {observations['subject']['display']}: systolic = {systolic}, diastolic = {diastolic}")
            
            return patient_id, systolic, diastolic, anomaly_type


        # Consommateur Kafka
        def consumer_kafka(observations): 
            c = Consumer({'bootstrap.servers': 'localhost:9092', 'group.id': 'python-consumers', 'auto.offset.reset': 'earliest'})
            c.subscribe(['blood_pressure_topic'])  # Topic Kafka où envoyer les données

            while True:
                msg = c.poll(1.0)
            
                if msg is None:
                    break
                if msg.error():
                    print("Consumer error: {}".format(msg.error()))
                    continue

                print('Message reçu : {}'.format(msg.value().decode('utf-8')))
                break

            c.close()

        consumer_kafka(observations)


        # Connexion à Elasticsearch
        es = Elasticsearch()

        def anomaly_elasticsearch(observations):
            patient_id, systolic, diastolic, anomaly_type = detect_anomaly(observations)  

            # Préparation des données d'anomalie, pour cela je crée un dictionnaire qui va contenir toute les valeurs dont on aura besoin pour visualiser nos donnée sur kibana
            anomaly_data = {'patient_id': patient_id,'systolic_pressure': systolic, 'diastolic_pressure': diastolic, 'anomaly_type': anomaly_type, 'date': random_date_str, 'sex': sexe}
            
            # j'ai rajouté cette ligne de commande car je recevai beacoup d'erreur 406 donc je essayé d'implémenter
            # une fonctionalité qui me permet de savoir qu'elle erreur serait retourner
            try:
                # Indexation des données dans Elasticsearch
                res = es.index(index="blood_pressure_anomalies_version_test", body=anomaly_data)
                print(f"Document indexé dans Elasticsearch : {res['_id']}")

            except Exception as e:
                print(f"Erreur lors de l'indexation : {e}")


        def save_normal_data(observations, filename):
            try:
                with open(filename, 'r') as file:
                    data = json.load(file)
            except FileNotFoundError: 
                data = []

            if isinstance(observations, list):
                data.extend(observations)
            else:
                data.append(observations)

            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
                
            print(f"Observation normale sauvegardée dans {filename}")


        # Vérification et envoi dans Elasticsearch ou sauvegarde du fichier
        anomaly_type = detect_anomaly(observations)[3]
        if anomaly_type in ["tension élevé" , "Hypertension de stade 1", "Hypertension de stade 2","Crise hypertensive (Urgence immédiate)", "Hypotension"]:
            print(f"Vérification : Anomalie détectée: {anomaly_type}")
            anomaly_elasticsearch(observations)
        if anomaly_type == "tension normale": 
            print("Observation normale")
            save_normal_data(observations, 'normal_blood_pressure.json')

