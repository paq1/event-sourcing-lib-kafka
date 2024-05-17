from event_sourcing.app.cqrs_component import CqrsComponent
from event_sourcing.app.kafka_command_engine import KafkaCommandEngine
from event_sourcing.models.command_test.command_creation_bob import CommandTest


class Component(CqrsComponent):
    def __init__(self):
        super().__init__()
        self.exemple_kafka_engine = KafkaCommandEngine[str, CommandTest, str](
            kafka_producer_handler=self.kafka_producer_handler,
            subscriptions=self.kafka_result_subscriptions,
            queue_producer_handler=self.kafka_producer_handler,
            ontology="subject"
        )

    def start(self):
        self.exemple_kafka_engine.start()
        return self

    def stop(self):
        self.exemple_kafka_engine.stop()
        return self
