import logging
import uuid

import asyncio

from event_sourcing.app.cqrs_component import CqrsComponent
from event_sourcing.logging_config import setup_logging
from event_sourcing.models.command import Command
from event_sourcing.models.command_test.command_creation_bob import CreerBobCommand
from exemple.app.components import Component

logger = logging.getLogger(__name__)


async def main(debug, logging_level):
    setup_logging(debug, logging_level)

    mode = "dev" if debug else "production"
    logging.getLogger(__name__).info(f"lancement du programme de test de la lib event sourcing en mode [{mode}]")

    component: Component = Component()
    component.listeners_kafka_handler.start_listeners()

    await asyncio.sleep(1)
    logger.info("debut du test sur les offers")
    await simulation_offer(component)

    # on arrete nos thread
    component.listeners_kafka_handler.stop_listeners()


async def simulation_offer(component: Component) -> None:
    command1 = Command(entityId=str(uuid.uuid4()), handler_name="creer-bob",
                       command=CreerBobCommand(nom="PAQUIN", prenom="Pierre"))

    traitement = await component.kafka_engine.offer(command=command1)
    logger.info(f'resultat du traitement : {traitement.result}')

    command2 = Command(entityId=str(uuid.uuid4()), handler_name="creer-bob",
                       command=CreerBobCommand(nom="DJAMA", prenom="Yoann"))

    traitement2 = await component.kafka_engine.offer(command=command2)
    logger.info(f'resultat 2 du traitement : {traitement2.result}')


if __name__ == "__main__":
    asyncio.run(main(debug=True, logging_level=logging.DEBUG))
    # run()
