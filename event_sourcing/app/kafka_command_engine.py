import logging
import uuid
from typing import Generic, TypeVar

from event_sourcing.app.kafka_result_subscription import KafkaResultSubscriptions, EnveloppeKafkaResult
from event_sourcing.core.queue_message_producer import QueueMessageProducerHandler

STATE = TypeVar('STATE')
COMMAND = TypeVar('COMMAND')
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

    async def offer(self) -> EnveloppeKafkaResult[SubjectResultKafka]:
        correlation_id = str(uuid.uuid4())
        self.logger.debug(f"[kafka-command-engin#offer] creation du correlation id : {correlation_id}")
        self.__subscriptions.subscribe(correlation_id)
        self.queue_producer_handler.produce_message_sync(
            {'ma_command': 'toto en slip'},
            "subject-cqrs-commands",  # fixme pas magique string
            key=correlation_id
        )

        result: EnveloppeKafkaResult[SubjectResultKafka] = self.__subscriptions.get(correlation_id).result(timeout=30)
        self.logger.debug(f"[kafka-command-engin#offer] correlation : {correlation_id}")
        self.__subscriptions.unsubscribe(correlation_id)
        return result
