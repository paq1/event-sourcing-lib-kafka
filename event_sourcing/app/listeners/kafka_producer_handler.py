import logging

from kafka import KafkaProducer

from event_sourcing.core.queue_message_producer import QueueMessageProducerHandler


class KafkaProducerHandler(QueueMessageProducerHandler):
    logger = logging.getLogger(f"{__name__}#KafkaProducerHandler")

    def __init__(self, kafka_producer: KafkaProducer):
        self.kafka_producer = kafka_producer

    def produce_message_sync(self, message: dict, topic: str, key: str) -> None:
        try:
            response_f = self.kafka_producer.send(topic=topic, key=key.encode(), value=message)
            _ = response_f.get(timeout=5)
            self.logger.debug("message sent successfully")
        except Exception as e:
            self.logger.error(e)
