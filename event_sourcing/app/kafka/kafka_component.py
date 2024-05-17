import json

from kafka import KafkaProducer, KafkaConsumer

from event_sourcing.app import KafkaResultSubscriptions, SubjectResultKafka, ListenersKafkaHandler
from event_sourcing.app.listeners.kafka_producer_handler import KafkaProducerHandler


class KafkaComponent:
    def __init__(
            self,
            ontology: str = "exemple",
            kafka_producer_host: str = "192.168.1.19:9092",
            kafka_consumer_host: str = "192.168.1.19:9092",
            group_id: str = "default-engine-consumer"
    ):
        self.kafka_producer = KafkaProducer(bootstrap_servers=kafka_producer_host,
                                            value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        self.kafka_consumer_commands: KafkaConsumer = KafkaConsumer(
            f"{ontology}-cqrs-commands",
            bootstrap_servers=f"{kafka_consumer_host}",
            group_id=f"{group_id}",
            auto_offset_reset="latest"
        )

        self.kafka_consumer_results: KafkaConsumer = KafkaConsumer(
            f"{ontology}-cqrs-results",
            bootstrap_servers=f"{kafka_consumer_host}",
            group_id=f"{group_id}",
            auto_offset_reset="latest"
        )

        self.kafka_producer_handler = KafkaProducerHandler(kafka_producer=self.kafka_producer)
        self.kafka_result_subscriptions = KafkaResultSubscriptions[SubjectResultKafka]()

        self.listeners_kafka_handler: ListenersKafkaHandler = ListenersKafkaHandler(self.kafka_result_subscriptions,
                                                                                    self.kafka_producer_handler)
