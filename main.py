import asyncio

from event_sourcing.app import *
import logging

from event_sourcing.logging_config import setup_logging

logger = logging.getLogger(__name__)


async def main(debug, logging_level):
    setup_logging(debug, logging_level)
    kafka_result_subscriptions = KafkaResultSubscriptions[SubjectResultKafka]()
    listeners_kafka_handler = ListenersKafkaHandler(kafka_result_subscriptions)
    listeners_kafka_handler.start_listeners()
    logger.debug("listener started")
    await asyncio.sleep(1)

    logger.info("debut du test sur les offers")
    kafka_engine = KafkaCommandEngine[str, str, str](subscriptions=kafka_result_subscriptions)
    traitement = await kafka_engine.offer()
    logger.info(f'resultat du traitement : {traitement.result}')
    traitement2 = await kafka_engine.offer()
    logger.info(f'resultat 2 du traitement : {traitement2.result}')

    # on arrete nos thread
    listeners_kafka_handler.stop_listeners()


if __name__ == "__main__":
    logger.info("test")
    asyncio.run(main(debug=True, logging_level=logging.DEBUG))
    logger.debug("test")
    #
    # print("fin main")
