import json
import logging
import uuid

import asyncio
from kafka import KafkaProducer

from event_sourcing.app import *
from event_sourcing.app import ListenersKafkaHandler
from event_sourcing.app.listeners.kafka_producer_handler import KafkaProducerHandler
from event_sourcing.concept_serde import run
from event_sourcing.logging_config import setup_logging
from event_sourcing.models.command import Command
from event_sourcing.models.command_test.command_creation_bob import CreerBobCommand, CommandTest

logger = logging.getLogger(__name__)


async def main(debug, logging_level):
    setup_logging(debug, logging_level)

    mode = "dev" if debug else "production"
    logging.getLogger(__name__).info(f"lancement du programme de test de la lib event sourcing en mode [{mode}]")

    kafka_producer = KafkaProducer(bootstrap_servers='192.168.1.61:9092',
                                   value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    kafka_producer_handler = KafkaProducerHandler(kafka_producer=kafka_producer)

    kafka_result_subscriptions = KafkaResultSubscriptions[SubjectResultKafka]()
    listeners_kafka_handler: ListenersKafkaHandler = ListenersKafkaHandler(kafka_result_subscriptions,
                                                                           kafka_producer_handler)
    listeners_kafka_handler.start_listeners()
    logger.debug("listener started")
    await asyncio.sleep(1)

    logger.info("debut du test sur les offers")
    kafka_engine = KafkaCommandEngine[str, CommandTest, str](subscriptions=kafka_result_subscriptions,
                                                     queue_producer_handler=kafka_producer_handler)

    command1 = Command(entityId=str(uuid.uuid4()), handler_name="creer-bob",
                       command=CreerBobCommand(nom="PAQUIN", prenom="Pierre"))
    traitement = await kafka_engine.offer(command=command1)
    logger.info(f'resultat du traitement : {traitement.result}')

    command2 = Command(entityId=str(uuid.uuid4()), handler_name="creer-bob",
                       command=CreerBobCommand(nom="DJAMA", prenom="Yoann"))
    traitement2 = await kafka_engine.offer(command=command2)
    logger.info(f'resultat 2 du traitement : {traitement2.result}')

    # on arrete nos thread
    listeners_kafka_handler.stop_listeners()


if __name__ == "__main__":
    # asyncio.run(main(debug=True, logging_level=logging.DEBUG))
    run()
