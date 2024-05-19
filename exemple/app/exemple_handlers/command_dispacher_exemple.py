from event_sourcing.app.command_handlers.command_dispacher import CommandDispatcher
from exemple.app.exemple_handlers.create_personne_handler import CreatePersonneHandler
from exemple.app.exemple_handlers.exemple_models import CommandApi, State, Event
from exemple.app.exemple_handlers.update_personne_handler import UpdatePersonneHandler


def create_command_dispatcher_exemple() -> CommandDispatcher[CommandApi, State, Event]:
    return (
        CommandDispatcher[CommandApi, State, Event]()
        .with_handler(
            CreatePersonneHandler()
        )
        .with_handler(
            UpdatePersonneHandler()
        )
    )
