from event_sourcing.app.command_handlers.command_dispacher import CommandDispacher
from event_sourcing.app.command_handlers.exemple_handlers.create_personne_handler import CreatePersonneHandler
from event_sourcing.app.command_handlers.exemple_handlers.exemple_models import CommandApi, State, Event


def create_command_dispatcher_exemple() -> CommandDispacher[CommandApi, State, Event]:
    return (
        CommandDispacher[CommandApi, State, Event]()
        .with_handler(
            CreatePersonneHandler()
        )
    )
