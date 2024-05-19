from event_sourcing.app.cqrs_component import CqrsComponent
from event_sourcing.app.kafka_command_engine import KafkaCommandEngine
from event_sourcing.models.command_test.command_creation_bob import CommandTest
from exemple.app.exemple_handlers.command_dispacher_exemple import create_command_dispatcher_exemple


class Component(CqrsComponent):
    def __init__(self):
        super().__init__()
        command_dispatcher = create_command_dispatcher_exemple()
        self.exemple_kafka_engine = KafkaCommandEngine[str, CommandTest, str](
            command_dispatcher=command_dispatcher,
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
