from event_sourcing.app.command_handlers.command_dispacher import CommandHandlerCreate
from event_sourcing.app.command_handlers.exemple_handlers.exemple_models import CommandCreate, State, Event, CreateEvent


class CreatePersonneHandler(CommandHandlerCreate[CommandCreate, State, Event]):
    def __init__(self):
        super().__init__("create_personne")

    async def on_command(self, cmd: CommandCreate, entityId: str) -> Event:
        return CreateEvent(by="usr:mkd", prenom=cmd.prenom, nom=cmd.nom)
