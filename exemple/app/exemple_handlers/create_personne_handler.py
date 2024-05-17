from event_sourcing.app.command_handlers.command_dispacher import CommandHandlerCreate
from exemple.app.exemple_handlers.exemple_models import CommandCreate, State, Event, CreateEvent
import logging


class CreatePersonneHandler(CommandHandlerCreate[CommandCreate, State, Event]):
    logger = logging.getLogger(f"{__name__}#CreatePersonneHandler")

    def __init__(self):
        super().__init__("create_personne")

    async def on_command(self, cmd: CommandCreate, entityId: str) -> Event:
        self.logger.debug("appel au command handler de creation de personne")
        return CreateEvent(by="usr:mkd", prenom=cmd.prenom, nom=cmd.nom)
