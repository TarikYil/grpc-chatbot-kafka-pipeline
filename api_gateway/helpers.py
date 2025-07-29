# api_gateway/helpers.py

from kafka import KafkaProducer, KafkaConsumer
import json

def create_kafka_producer():
    """Create and return a Kafka producer."""
    return KafkaProducer(
        bootstrap_servers="kafka:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

def consume_responses(responses):
    """Consume responses from Kafka and store them in a dictionary."""
    consumer = KafkaConsumer(
        'prompt-responses',
        bootstrap_servers='kafka:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id="api-resp-group"
    )
    for msg in consumer:
        res = msg.value
        req_id = res["request_id"]
        responses[req_id] = res["response"]