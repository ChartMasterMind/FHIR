import json
from confluent_kafka import Producer


def produce_to_kafka(observations):
            producer = Producer({'bootstrap.servers': 'localhost:9092'})

            OBS_JSON = json.dumps(observations)  # Convertir le dict en JSON, nécessaire pour produire avec Kafka
            producer.produce('blood_pressure_topic_final_1', value=OBS_JSON) # definition de notre topic kafka où envoyer les données.

            print("Observation envoyée à Kafka")
            producer.flush()
