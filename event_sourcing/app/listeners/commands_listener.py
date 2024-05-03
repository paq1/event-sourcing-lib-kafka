import logging
from typing import Generic, TypeVar

from kafka import KafkaConsumer, KafkaProducer

T = TypeVar('T')


class CommandsListener(Generic[T]):
    logger = logging.getLogger(f"{__name__}#CommandsListener")

    def __init__(self, topic_commands_name: str, producer: KafkaProducer):
        self.consumer = KafkaConsumer(
            topic_commands_name,
            bootstrap_servers='192.168.1.61:9092',
            group_id=f"consumer_cqrs_grp_2",
            auto_offset_reset="latest"  # "earliest"
        )
        self.producer = producer
        self.running = True

    def run(self):
        for msg in self.consumer:
            key = msg.key.decode('utf-8')
            self.logger.debug(f"received message {key}")
            self.logger.debug(f"traitement de la command : {key}")
            # mkdmkd todo traitement de la command ici avec le command dispatcher
            # mkdmkd todo insertion en db

            message_send_f = self.__produce(
                topic="subject-cqrs-results",
                message={"result": "autre donnees"},
                key=key
            )

            if message_send_f.succeeded():
                self.logger.debug("message sent successfully")
            else:
                self.logger.error("message sent failed")

            if not self.running:
                self.logger.info("stopping loop")
                break
        self.logger.info("thread finished")

    def stop(self):
        self.running = False

    def __produce(self, message: dict, topic: str, key: str):
        response_f = self.producer.send(topic=topic, key=key.encode(), value=message)
        return response_f
