import json

from kafka import KafkaProducer

from event_sourcing.app.kafka_command_engine import SubjectResultKafka
from event_sourcing.app.kafka_result_subscription import KafkaResultSubscriptions
from event_sourcing.app.listeners.kafka_producer_handler import KafkaProducerHandler


class KafkaComponent:
    def __init__(
            self,
            kafka_producer_host: str = "192.168.1.19:9092",
    ):
        self.kafka_producer = KafkaProducer(bootstrap_servers=kafka_producer_host,
                                            value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        self.kafka_producer_handler = KafkaProducerHandler(kafka_producer=self.kafka_producer)
        self.kafka_result_subscriptions = KafkaResultSubscriptions[SubjectResultKafka]()
