import json
import uuid
from typing import Generic, TypeVar

import asyncio
from kafka import KafkaProducer
from kafka.producer.future import FutureRecordMetadata

from event_sourcing.app.kafka_result_subscription import KafkaResultSubscriptions, EnveloppeKafkaResult

STATE = TypeVar('STATE')
COMMAND = TypeVar('COMMAND')
EVENT = TypeVar('EVENT')


class SubjectResultKafka(object):
    def __init__(self, key: str, content: dict[str, str]):
        self.key = key
        self.content = content

    def __str__(self):
        return f"[{self.key}]: {self.content}"


class KafkaCommandEngine(Generic[STATE, COMMAND, EVENT]):
    def __init__(self, subscriptions: KafkaResultSubscriptions[SubjectResultKafka],
                 topic_name: str = "subject-cqrs-commands"):
        self.producer = KafkaProducer(bootstrap_servers='192.168.1.61:9092',
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        self.topic_commands_name: str = topic_name

        self.__subscriptions = subscriptions

    async def offer(self) -> EnveloppeKafkaResult[SubjectResultKafka]:
        correlation_id = str(uuid.uuid4())
        print(f"[kafka-command-engin#offer] creation du correlation id : {correlation_id}")
        self.__subscriptions.subscribe(correlation_id)
        produce: FutureRecordMetadata = self.__produce(
            {'ma_command': 'toto en slip'},
            "subject-cqrs-commands",  # fixme pas magique string
            key=correlation_id
        )
        await asyncio.sleep(1)
        if produce.succeeded():
            print("[kafka-command-engin#offer] successfully produced message command")
        else:
            print("failed to produce a message")
        result: EnveloppeKafkaResult[SubjectResultKafka] = self.__subscriptions.get(correlation_id).result(timeout=30)
        print(f"[kafka-command-engin#offer] correlation : {correlation_id}")
        self.__subscriptions.unsubscribe(correlation_id)
        return result

    def __produce(self, message: dict, topic: str, key: str):
        response_f = self.producer.send(topic=topic, key=key.encode(), value=message)
        return response_f
