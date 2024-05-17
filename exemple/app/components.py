from event_sourcing.app import KafkaCommandEngine
from event_sourcing.app.cqrs_component import CqrsComponent
from event_sourcing.models.command_test.command_creation_bob import CommandTest


class Component(CqrsComponent):
    def __init__(self):
        super().__init__()
        self.kafka_engine = KafkaCommandEngine[str, CommandTest, str](
            subscriptions=self.kafka_result_subscriptions,
            queue_producer_handler=self.kafka_producer_handler
        )
