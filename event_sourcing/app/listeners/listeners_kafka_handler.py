import json

from kafka import KafkaProducer

from event_sourcing.app.kafka_command_engine import SubjectResultKafka
from event_sourcing.app.kafka_result_subscription import KafkaResultSubscriptions
from event_sourcing.app.listeners import CommandsListener, ResultsListener
from event_sourcing.app.listeners.threads import ThreadListenerCommands, ThreadListenerResults


class ListenersKafkaHandler(object):
    def __init__(self, kafka_result_subscriptions: KafkaResultSubscriptions[SubjectResultKafka]):
        self.kafka_producer = KafkaProducer(bootstrap_servers='192.168.1.61:9092',
                                            value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        commands_listener: CommandsListener[str] = CommandsListener(
            "subject-cqrs-commands",
            self.kafka_producer
        )
        results_listener: ResultsListener[str] = ResultsListener(
            "subject-cqrs-results",
            subscriptions=kafka_result_subscriptions
        )

        self.th_commands_listener = ThreadListenerCommands(commands_listener)
        self.th_results_listener = ThreadListenerResults(results_listener)

    def start_listeners(self):
        self.th_commands_listener.start()
        self.th_results_listener.start()

    def stop_listeners(self):
        self.th_commands_listener.stop()
        self.th_results_listener.stop()
        self.th_commands_listener.join()
        self.th_results_listener.join()
