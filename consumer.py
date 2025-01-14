
import json
from confluent_kafka import Consumer, Producer
from elasticsearch import Elasticsearch




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


def consumer_kafka(): 
            c = Consumer({'bootstrap.servers': 'localhost:9092', 'group.id': 'python-consumers', 'auto.offset.reset': 'earliest'})
            c.subscribe(['blood_pressure_topic_7'])  # Topic Kafka où sont stocker les données du producteur

            while True:
                msg = c.poll(3.0)
            
                if msg is None:
                    break
                if msg.error():
                    print("Consumer error: {}".format(msg.error()))
                    continue

                print('Message reçu : {}'.format(msg.value().decode('utf-8')))
                break

            c.close()

        # Connexion à Elasticsearch et indexation des données
        # Connexion à Elasticsearch et indexation des données
            es = Elasticsearch()

            msg = json.loads(msg.value().decode('utf-8'))

            anomaly_type = detect_anomaly(msg)

            systolic = msg['component'][0]['valueQuantity']['value']
            diastolic = msg['component'][1]['valueQuantity']['value']
            patient_id = msg['id']
            patient_name = msg['subject']['display']
            random_date_str = msg["effectiveDateTime"]

            anomaly_type = detect_anomaly(msg)

            if anomaly_type in ["tension élevé" , "Hypertension de stade 1", "Hypertension de stade 2","Crise hypertensive (Urgence immédiate)", "Hypotension"]:
                print(f"Vérification : Anomalie détectée: {anomaly_type}")

                anomaly_type = detect_anomaly(msg)
            
            # Préparation des données d'anomalie, pour cela je crée un dictionnaire qui va contenir toute les valeurs dont on aura besoin pour visualiser nos donnée sur kibana.
                anomaly_data = {'patient_id': patient_id,'patient_name': patient_name ,'systolic_pressure': systolic, 'diastolic_pressure': diastolic, 'anomaly_type': anomaly_type, 'date': random_date_str}
            
            # j'ai rajouté cette ligne de commande car je recevai beacoup d'erreur 406 donc je essayé d'implémenter
            # une fonctionalité qui me permet de savoir qu'elle erreur serait retourner
                try:
                # Indexation des données dans Elasticsearch
                    res = es.index(index="blood_pressure_anomalies_version_test_test", body=anomaly_data)
                    print(f"Document indexé dans Elasticsearch : {res['_id']}")

                except Exception as e:
                    print(f"Erreur lors de l'indexation : {e}")
            
            if anomaly_type == "tension normale": 
                print("Observation normale")
                save_normal_data(msg, 'normal_blood_pressure.json')

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


consumer_kafka()


       