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
        for msg in self.consumer:
            key: str = msg.key.decode('utf-8')
            print(msg)
            print(f"[ResultsListener] traitement du message de resultat : {key}")
            # mkdmkd todo traitement de la command ici
            correlation_id: str = key
            print(f"[ResultsListener] correlation_id : {correlation_id}")
            print("keys :")
            print(self.subscriptions.subscriptions.keys())
            try:
                promesse: Future[EnveloppeKafkaResult[SubjectResultKafka]] = self.subscriptions.get(correlation_id)
                promesse.set_result(
                    EnveloppeKafkaResult[SubjectResultKafka](
                        SubjectResultKafka(correlation_id, {"msg": "gg a toi"})
                    )
                )
            except Exception:
                print(
                    f"[ResultsListener#run#exception] pas de souscription en cours pour le correlation id : {correlation_id}"
                )

            if not self.running:
                print("[ResultsListener] stopping loop")
                break
        print("[ResultsListener] MKDMKD - thread finished")

    def stop(self):
        print("[results-listener] stop")
        self.running = False
        self.consumer.close()
