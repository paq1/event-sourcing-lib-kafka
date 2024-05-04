import logging
import uuid
from typing import Generic, TypeVar

from event_sourcing.app.kafka_result_subscription import KafkaResultSubscriptions, EnveloppeKafkaResult
from event_sourcing.core.queue_message_producer import QueueMessageProducerHandler
from event_sourcing.models.command import Command
from event_sourcing.models.has_schema import HasSchema

STATE = TypeVar('STATE')
COMMAND = TypeVar('COMMAND', bound=HasSchema)
EVENT = TypeVar('EVENT')


class SubjectResultKafka(object):
    def __init__(self, key: str, content: dict[str, str]):
        self.key = key
        self.content = content

    def __str__(self):
        return f"[{self.key}]: {self.content}"


class KafkaCommandEngine(Generic[STATE, COMMAND, EVENT]):
    logger = logging.getLogger(f"{__name__}#KafkaCommandEngine")

    def __init__(
            self,
            subscriptions: KafkaResultSubscriptions[SubjectResultKafka],
            queue_producer_handler: QueueMessageProducerHandler,
            topic_name: str = "subject-cqrs-commands",
    ):
        self.queue_producer_handler = queue_producer_handler

        self.topic_commands_name: str = topic_name

        self.__subscriptions = subscriptions

    async def offer(self, command: Command[COMMAND]) -> EnveloppeKafkaResult[SubjectResultKafka]:
        correlation_id = str(uuid.uuid4())
        self.logger.debug(f"[kafka-command-engin#offer] creation du correlation id : {correlation_id}")
        self.__subscriptions.subscribe(correlation_id)
        self.queue_producer_handler.produce_message_sync(
            self.__from_command_to_record(command),
            "subject-cqrs-commands",  # fixme pas de magic string
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
