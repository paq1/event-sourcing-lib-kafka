from concurrent.futures import Future
from typing import Generic, TypeVar

from kafka import KafkaConsumer

from event_sourcing.app.kafka_command_engine import SubjectResultKafka
from event_sourcing.app.kafka_result_subscription import KafkaResultSubscriptions, EnveloppeKafkaResult

T = TypeVar('T')


class ResultsListener(Generic[T]):
    def __init__(self, topic_commands_name: str, subscriptions: KafkaResultSubscriptions[SubjectResultKafka]):
        self.consumer = KafkaConsumer(
            topic_commands_name,
            bootstrap_servers='192.168.1.61:9092',
            group_id=f"consumer_cqrs_grp_2",
            auto_offset_reset="latest"  # "earliest"
        )
        self.subscriptions = subscriptions
        self.running = True

    def run(self):
        while self.running:
            for msg in self.consumer:
                key: str = msg.key.decode('utf-8')
                print(msg)
                print(f"[results-listener] traitement de la command : {key}")
                # mkdmkd todo traitement de la command ici
                correlation_id: str = key
                print(f"[results-listener] correlation_id : {correlation_id}")
                print("keys :")
                print(self.subscriptions.subscriptions.keys())
                promesse: Future[EnveloppeKafkaResult[SubjectResultKafka]] = self.subscriptions.get(correlation_id)
                promesse.set_result(
                    EnveloppeKafkaResult[SubjectResultKafka](
                        SubjectResultKafka(correlation_id, {"msg": "gg a toi"})
                    )
                )
                if not self.running:
                    print("[commands-listener] stopping loop")
                    break

    def stop(self):
        print("[results-listener] stop")
        self.running = False
        self.consumer.close()
