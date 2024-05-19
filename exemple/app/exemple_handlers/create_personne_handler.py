from event_sourcing.app.command_handlers.command_dispacher import CommandHandlerCreate
from exemple.app.exemple_handlers.exemple_models import CommandCreate, State, Event, CreatePersonneEvent
import logging


class CreatePersonneHandler(CommandHandlerCreate[CommandCreate, State, Event]):
    logger = logging.getLogger(f"{__name__}#CreatePersonneHandler")

    def __init__(self):
        super().__init__("create_personne")

    def validate_command(self, cmd: dict) -> CommandCreate | None:
        try:
            return CommandCreate(cmd["nom"], cmd["prenom"])
        except Exception as e:
            self.logger.error(e)
            return None

    async def on_command(self, cmd: CommandCreate, entityId: str) -> Event:
        self.logger.debug("appel au command handler de creation de personne")
        return CreatePersonneEvent(by="usr:mkd", prenom=cmd.prenom, nom=cmd.nom)
