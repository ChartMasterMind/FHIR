import json
from confluent_kafka import Consumer
from elasticsearch import Elasticsearch

# Fonction pour détecter une anomalie
def detect_anomaly(observation):
    systolic = observation['component'][0]['valueQuantity']['value']
    diastolic = observation['component'][1]['valueQuantity']['value']

    anomaly_type = "tension normale"

    if systolic >= 120 and systolic <= 129 and diastolic < 80:
        anomaly_type = "tension élevé"
    elif systolic > 180 or diastolic > 120:
        anomaly_type = "Crise hypertensive (Urgence immédiate)"
    elif systolic >= 140 or diastolic >= 90:
        anomaly_type = "Hypertension de stade 2"
    elif systolic >= 130 and systolic <= 139 or diastolic >= 80 and diastolic <= 89:
        anomaly_type = "Hypertension de stade 1"
    elif systolic < 90 or diastolic < 60:
        anomaly_type = "Hypotension"

    return anomaly_type

# Fonction pour sauvegarder les données normales
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

# Fonction principale pour consommer les messages Kafka
def consumer_kafka():
    # Configuration du consommateur Kafka
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'python-consumers',
        'auto.offset.reset': 'earliest'
    })

    # Souscription au topic
    consumer.subscribe(['blood_pressure_topic_final_1'])

    # Connexion à Elasticsearch
    es = Elasticsearch()

    try:
        print("En attente des messages...")
        while True:
            msg = consumer.poll(1.0) 
            
            if msg is None:  
                continue

            # Traitement du message
            message_data = json.loads(msg.value().decode('utf-8'))
            print(f"Message reçu : {message_data}")

            anomaly_type = detect_anomaly(message_data)
            systolic = message_data['component'][0]['valueQuantity']['value']
            diastolic = message_data['component'][1]['valueQuantity']['value']
            patient_id = message_data['id']
            patient_name = message_data['subject']['display']
            random_date_str = message_data["effectiveDateTime"]

            # Préparation des données pour Elasticsearch
            anomaly_data = {
                'patient_id': patient_id,
                'patient_name': patient_name,
                'systolic_pressure': systolic,
                'diastolic_pressure': diastolic,
                'anomaly_type': anomaly_type,
                'date': random_date_str
            }

            if anomaly_type != "tension normale":
                print(f"Anomalie détectée : {anomaly_type}")
                try:
                    # Indexation des données dans Elasticsearch
                    res = es.index(index="blood_pressure_anomalies_version_final_project", body=anomaly_data)
                    print(f"Document indexé dans Elasticsearch : {res['_id']}")
                except Exception as e:
                    print(f"Erreur lors de l'indexation : {e}")
            else:
                print("Observation normale")
                save_normal_data(message_data, 'normal_blood_pressure.json')

    # j'ai rajouté cette ligne car parfois j'avais des errerus mais rien ne s'afficher
    except KeyboardInterrupt:
        print("Arrêt du consommateur Kafka.")
    finally:
        
        consumer.close()


consumer_kafka()
