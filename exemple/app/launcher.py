import logging
import uuid

import asyncio

from event_sourcing.logging_config import setup_logging
from event_sourcing.models.command import Command
from exemple.app.components import Component

logger = logging.getLogger(__name__)


async def main(debug, logging_level):
    setup_logging(debug, logging_level)

    mode = "dev" if debug else "production"
    logging.getLogger(__name__).info(f"lancement du programme de test de la lib event sourcing en mode [{mode}]")

    component: Component = Component().start()

    await asyncio.sleep(1)
    logger.info("debut du test sur les offers")
    await simulation_offer(component)

    # on arrete nos thread
    component.stop()


async def simulation_offer(component: Component) -> None:
    command1 = Command(entityId=str(uuid.uuid4()), handler_name="create_personne",
                       data={"nom": "PAQUIN", "prenom": "Pierre"})

    traitement = await component.exemple_kafka_engine.offer(command=command1)
    logger.info(f'resultat du traitement : {traitement.result}')

    command2 = Command(entityId=str(uuid.uuid4()), handler_name="update_personne",
                       data={"nom": "DJAMA", "prenom": "Yoann"})

    traitement2 = await component.exemple_kafka_engine.offer(command=command2)
    logger.info(f'resultat 2 du traitement : {traitement2.result}')


if __name__ == "__main__":
    asyncio.run(main(debug=True, logging_level=logging.DEBUG))
