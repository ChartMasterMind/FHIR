import json
from confluent_kafka import Producer


def produce_to_kafka(observations):
            producer = Producer({'bootstrap.servers': 'localhost:9092'})

            producer.produce('blood_pressure_topic_final_1', value=observations) # definition de notre topic kafka où envoyer les données.

            print("Observation envoyée à Kafka")
            producer.flush()
