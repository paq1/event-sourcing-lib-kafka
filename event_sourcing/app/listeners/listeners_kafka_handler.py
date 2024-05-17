import logging

from event_sourcing.app.kafka.enveloppe_kafka import SubjectResultKafka
from event_sourcing.app.kafka_result_subscription import KafkaResultSubscriptions
from event_sourcing.app.listeners.commands_listener import CommandsListener
from event_sourcing.app.listeners.results_listener import ResultsListener
from event_sourcing.app.listeners.threads import ThreadListenerCommands, ThreadListenerResults
from event_sourcing.core.queue_message_producer import QueueMessageProducerHandler


class ListenersKafkaHandler(object):
    logger = logging.getLogger(f"{__name__}#ListenersKafkaHandler")

    def __init__(self, kafka_result_subscriptions: KafkaResultSubscriptions[SubjectResultKafka],
                 queue_message_producer: QueueMessageProducerHandler):
        commands_listener: CommandsListener[str] = CommandsListener(
            "subject-cqrs-commands",
            queue_message_producer
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
        self.logger.info("listeners started")

    def stop_listeners(self):
        self.th_commands_listener.stop()
        self.th_results_listener.stop()
        self.th_commands_listener.join()
        self.th_results_listener.join()
