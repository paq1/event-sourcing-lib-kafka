import logging
import uuid
from typing import Generic, TypeVar

from kafka import KafkaConsumer

from event_sourcing.app.kafka.enveloppe_kafka import SubjectResultKafka
from event_sourcing.app.listeners.listeners_kafka_handler import ListenersKafkaHandler
from event_sourcing.app.kafka_result_subscription import KafkaResultSubscriptions, EnveloppeKafkaResult
from event_sourcing.app.listeners.kafka_producer_handler import KafkaProducerHandler
from event_sourcing.core.queue_message_producer import QueueMessageProducerHandler
from event_sourcing.models.command import Command
from event_sourcing.models.has_schema import HasSchema

STATE = TypeVar('STATE')
COMMAND = TypeVar('COMMAND', bound=HasSchema)
EVENT = TypeVar('EVENT')


class KafkaCommandEngine(Generic[STATE, COMMAND, EVENT]):
    logger = logging.getLogger(f"{__name__}#KafkaCommandEngine")

    def __init__(
            self,
            kafka_producer_handler: KafkaProducerHandler,
            subscriptions: KafkaResultSubscriptions[SubjectResultKafka],
            queue_producer_handler: QueueMessageProducerHandler,
            ontology: str = "subject",
            servers: str = "192.168.1.19:9092",
            group_id: str = "default-engine-consumer",
    ):
        self.queue_producer_handler = queue_producer_handler

        self.topic_commands_name: str = f"{ontology}-cqrs-commands"
        self.topic_results_name: str = f"{ontology}-cqrs-results"

        self.kafka_consumer_commands: KafkaConsumer = KafkaConsumer(
            self.topic_commands_name,
            bootstrap_servers=servers,
            group_id=group_id,
            auto_offset_reset="latest"
        )

        self.kafka_consumer_results: KafkaConsumer = KafkaConsumer(
            self.topic_results_name,
            bootstrap_servers=servers,
            group_id=f"{group_id}",
            auto_offset_reset="latest"
        )

        self.listeners_kafka_handler: ListenersKafkaHandler = ListenersKafkaHandler(subscriptions,
                                                                                    kafka_producer_handler)

        self.__subscriptions = subscriptions

    async def offer(self, command: Command[COMMAND]) -> EnveloppeKafkaResult[SubjectResultKafka]:
        correlation_id = str(uuid.uuid4())
        self.logger.debug(f"[kafka-command-engin#offer] creation du correlation id : {correlation_id}")
        self.__subscriptions.subscribe(correlation_id)
        self.queue_producer_handler.produce_message_sync(
            self.__from_command_to_record(command),
            self.topic_commands_name,
            key=correlation_id
        )

        result: EnveloppeKafkaResult[SubjectResultKafka] = self.__subscriptions.get(correlation_id).result(timeout=30)
        self.logger.debug(f"[kafka-command-engin#offer] correlation : {correlation_id}")
        self.__subscriptions.unsubscribe(correlation_id)
        return result

    @staticmethod
    def __from_command_to_record(command: Command[COMMAND]) -> dict:
        return {
            "name": command.handler_name,
            "body": command.command.schema(),
            "entityId": command.entityId,
        }

    def start(self):
        self.listeners_kafka_handler.start_listeners()
        return self

    def stop(self):
        self.listeners_kafka_handler.stop_listeners()
        return self
