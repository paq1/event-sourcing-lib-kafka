from concurrent.futures import Future
from typing import Generic, TypeVar
import logging
T = TypeVar('T')


class EnveloppeKafkaResult(Generic[T]):
    def __init__(self, result: T):
        self.result = result


class KafkaResultSubscriptions(Generic[T]):
    logger = logging.getLogger(f"{__name__}#KafkaResultSubscriptions")

    def __init__(self):
        self.subscriptions: dict[str, Future[EnveloppeKafkaResult[T]]] = {}

    def subscribe(self, correlation_id: str):
        enveloppe_f: Future[EnveloppeKafkaResult[T]] = Future()
        # lance le process de souscription
        self.add((correlation_id, enveloppe_f))

    def add(self, subscription: (str, Future[EnveloppeKafkaResult[T]])):
        self.subscriptions[subscription[0]] = subscription[1]

    def unsubscribe(self, correlation_id: str):
        self.subscriptions.pop(correlation_id)

    def get(self, correlation_id: str) -> Future[EnveloppeKafkaResult[T]]:
        self.logger.debug(f"try get with id {correlation_id}")
        self.logger.debug(f"try get from {self.subscriptions.keys()}")
        return self.subscriptions[correlation_id]
