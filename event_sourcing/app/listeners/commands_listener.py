from typing import Generic, TypeVar

from kafka import KafkaConsumer, KafkaProducer

T = TypeVar('T')


class CommandsListener(Generic[T]):
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
        print("MKDMKD - running loop")
        for msg in self.consumer:
            key = msg.key.decode('utf-8')
            print(f"[CommandsListener] received message {key}")
            print(f"[CommandsListener] traitement de la command : {key}")
            # mkdmkd todo traitement de la command ici avec le command dispatcher
            # mkdmkd todo insertion en db

            message_send_f = self.__produce(
                topic="subject-cqrs-results",
                message={"result": "autre donnees"},
                key=key
            )

            if message_send_f.succeeded():
                print("[CommandsListener] message sent successfully")
            else:
                print("[CommandsListener] message sent failed")

            if not self.running:
                print("[CommandsListener] stopping loop")
                break
        print("[CommandsListener] MKDMKD - thread finished")

    def stop(self):
        print("[commands-listener] stop")
        self.running = False
        self.consumer.close()

    def __produce(self, message: dict, topic: str, key: str):
        response_f = self.producer.send(topic=topic, key=key.encode(), value=message)
        return response_f
