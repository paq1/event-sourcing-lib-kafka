from event_sourcing.app.command_handlers.command_dispacher import CommandDispatcher
from exemple.app.exemple_handlers.create_personne_handler import CreatePersonneHandler
from exemple.app.exemple_handlers.exemple_models import CommandApi, State, Event


def create_command_dispatcher_exemple() -> CommandDispatcher[CommandApi, State, Event]:
    return (
        CommandDispatcher[CommandApi, State, Event]()
        .with_handler(
            CreatePersonneHandler()
        )
    )
