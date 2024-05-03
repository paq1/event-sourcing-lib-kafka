from threading import Thread

import asyncio
from kafka import KafkaProducer
import json

from event_sourcing.app.kafka_command_engine import KafkaCommandEngine, SubjectResultKafka
from event_sourcing.app.kafka_result_subscription import KafkaResultSubscriptions
from event_sourcing.app.listeners.commands_listener import CommandsListener
from event_sourcing.app.listeners.results_listener import ResultsListener


class ThreadListenerCommands(Thread):
    def __init__(self, commands_listener: CommandsListener[str]):
        super().__init__()
        self.commands_listener = commands_listener

    def run(self):
        self.commands_listener.run()

    def stop(self):
        print("[ThreadListenerCommands#stop] Stopping listener...")
        self.commands_listener.stop()
        print("[ThreadListenerCommands#stop] listener stopped")


class ThreadListenerResults(Thread):
    def __init__(self, results_listener: ResultsListener[str]):
        Thread.__init__(self)
        self.results_listener = results_listener

    def run(self):
        self.results_listener.run()

    def stop(self):
        print("[ThreadListenerCommands#stop] Stopping listener...")
        self.results_listener.stop()
        print("[ThreadListenerCommands#stop] listener stopped")


async def main():
    kafka_producer = KafkaProducer(bootstrap_servers='192.168.1.61:9092',
                                   value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    kafka_subscriptions: KafkaResultSubscriptions[SubjectResultKafka] = KafkaResultSubscriptions()
    commands_listener: CommandsListener[str] = CommandsListener(
        "subject-cqrs-commands",
        kafka_producer
    )
    results_listener: ResultsListener[str] = ResultsListener(
        "subject-cqrs-results",
        subscriptions=kafka_subscriptions
    )

    th_commands_listener = ThreadListenerCommands(commands_listener)
    th_results_listener = ThreadListenerResults(results_listener)

    th_commands_listener.start()
    th_results_listener.start()

    print("listener started")
    await asyncio.sleep(1)
    print("begin offer")
    kafka_engine = KafkaCommandEngine[str, str, str](subscriptions=kafka_subscriptions)
    traitement = await kafka_engine.offer()
    print(f'resultat du traitement : {traitement.result}')
    traitement2 = await kafka_engine.offer()
    print(f'resultat 2 du traitement : {traitement2.result}')

    # on arrete nos thread
    th_commands_listener.stop()
    th_results_listener.stop()
    # th_commands_listener.join()
    # th_results_listener.join()


if __name__ == "__main__":
    asyncio.run(main())
    print("fin main")
