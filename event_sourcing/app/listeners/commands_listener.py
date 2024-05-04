import logging
from typing import Generic, TypeVar

from kafka import KafkaConsumer

from event_sourcing.core.queue_message_producer import QueueMessageProducerHandler

T = TypeVar('T')


class CommandsListener(Generic[T]):
    logger = logging.getLogger(f"{__name__}#CommandsListener")

    def __init__(self, topic_commands_name: str, queue_message_producer_handler: QueueMessageProducerHandler):
        self.consumer = KafkaConsumer(
            topic_commands_name,
            bootstrap_servers='192.168.1.61:9092',
            group_id=f"consumer_cqrs_grp_2",
            auto_offset_reset="latest"  # "earliest"
        )
        self.queue_message_producer_handler = queue_message_producer_handler
        self.running = True

    def run(self):
        for msg in self.consumer:
            key = msg.key.decode('utf-8')
            self.logger.debug(f"received message {key}")
            self.logger.debug(f"traitement de la command : {key}")
            # mkdmkd todo traitement de la command ici avec le command dispatcher
            # mkdmkd todo insertion en db

            self.queue_message_producer_handler.produce_message_sync(
                topic="subject-cqrs-results",
                message={"result": "autre donnees"},
                key=key
            )

            if not self.running:
                self.logger.info("stopping loop")
                break
        self.logger.info("thread finished")

    def stop(self):
        self.running = False
