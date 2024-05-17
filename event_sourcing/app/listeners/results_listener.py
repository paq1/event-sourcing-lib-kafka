import logging
from concurrent.futures import Future
from typing import Generic, TypeVar

from kafka import KafkaConsumer

from event_sourcing.app.kafka.enveloppe_kafka import SubjectResultKafka
from event_sourcing.app.kafka_result_subscription import KafkaResultSubscriptions, EnveloppeKafkaResult

T = TypeVar('T')


class ResultsListener(Generic[T]):
    logger = logging.getLogger(f"{__name__}#ResultsListener")

    def __init__(self, topic_commands_name: str, subscriptions: KafkaResultSubscriptions[SubjectResultKafka]):
        self.consumer = KafkaConsumer(
            topic_commands_name,
            bootstrap_servers='192.168.1.19:9092',
            group_id=f"consumer_cqrs_grp_2",
            auto_offset_reset="latest"  # "earliest"
        )
        self.subscriptions = subscriptions
        self.running = True

    def run(self):
        for msg in self.consumer:
            key: str = msg.key.decode('utf-8')
            self.logger.debug(msg)
            self.logger.debug(f"traitement du message de resultat : {key}")
            # mkdmkd todo traitement du resultat ici
            correlation_id: str = key
            self.logger.debug(f"correlation_id : {correlation_id}")
            try:
                promesse: Future[EnveloppeKafkaResult[SubjectResultKafka]] = self.subscriptions.get(correlation_id)
                promesse.set_result(
                    EnveloppeKafkaResult[SubjectResultKafka](
                        SubjectResultKafka(correlation_id, {"msg": "gg a toi"})
                    )
                )
            except Exception:
                self.logger.warning(
                    f"pas de souscription en cours pour le correlation id : {correlation_id}"
                )

            if not self.running:
                self.logger.info("stopping loop")
                break
        self.logger.info("thread finished")

    def stop(self):
        self.running = False
