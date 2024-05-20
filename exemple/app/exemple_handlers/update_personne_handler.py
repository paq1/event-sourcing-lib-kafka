import logging
from typing import Optional

from event_sourcing.app.command_handlers.command_handler import CommandHandlerUpdate
from exemple.app.exemple_handlers.exemple_models import Event, CommandUpdate, PersonneState, UpdatePersonneEvent


class UpdatePersonneHandler(CommandHandlerUpdate[CommandUpdate, PersonneState, Event]):
    logger = logging.getLogger(f"{__name__}#UpdatePersonneHandler")

    def __init__(self):
        super().__init__("update_personne")

    def validate_command(self, cmd: dict) -> Optional[CommandUpdate]:
        try:
            return CommandUpdate(cmd["nom"], cmd["prenom"])  # fixme prendre en compte l'optional
        except Exception as e:
            self.logger.error(e)
            return None

    async def on_command(self, cmd: CommandUpdate, entityId: str, state: PersonneState) -> Event:
        self.logger.debug("appel au command handler de creation de personne")
        return UpdatePersonneEvent(by="usr:mkd", prenom=cmd.prenom, nom=cmd.nom)
