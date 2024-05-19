import logging
from typing import TypeVar, Generic

from event_sourcing.app.command_handlers.command_dispacher import CommandDispatcher
from event_sourcing.app.kafka.enveloppe_kafka import SubjectResultKafka
from event_sourcing.app.kafka_result_subscription import KafkaResultSubscriptions
from event_sourcing.app.listeners.commands_listener import CommandsListener
from event_sourcing.app.listeners.results_listener import ResultsListener
from event_sourcing.app.listeners.threads import ThreadListenerCommandsHandler, ThreadListenerResults
from event_sourcing.core.queue_message_producer import QueueMessageProducerHandler

COMMAND = TypeVar('COMMAND')
STATE = TypeVar('STATE')
EVENT = TypeVar('EVENT')


class ListenersKafkaHandler(Generic[STATE, COMMAND, EVENT]):
    logger = logging.getLogger(f"{__name__}#ListenersKafkaHandler")

    def __init__(
            self, kafka_result_subscriptions: KafkaResultSubscriptions[SubjectResultKafka],
            queue_message_producer: QueueMessageProducerHandler,
            command_dispatcher: CommandDispatcher[STATE, COMMAND, EVENT]
    ):
        commands_listener: CommandsListener[STATE, COMMAND, EVENT] = CommandsListener(
            "subject-cqrs-commands",
            queue_message_producer,
            command_dispatcher
        )
        results_listener: ResultsListener[str] = ResultsListener(
            "subject-cqrs-results",
            subscriptions=kafka_result_subscriptions
        )

        self.th_commands_listener: ThreadListenerCommandsHandler[STATE, COMMAND, EVENT] = ThreadListenerCommandsHandler(
            commands_listener)
        self.th_results_listener = ThreadListenerResults(results_listener)

    def start_listeners(self):
        self.th_commands_listener.start()
        self.th_results_listener.start()
        self.logger.info("listeners started")

    def stop_listeners(self):
        self.th_commands_listener.stop()
        self.th_results_listener.stop()
        self.th_commands_listener.stop()
        self.th_results_listener.join()
