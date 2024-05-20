from typing import Generic, TypeVar, Optional

COMMAND = TypeVar('COMMAND')
STATE = TypeVar('STATE')
EVENT = TypeVar('EVENT')


class CommandHandler(Generic[STATE, COMMAND, EVENT]):
    def __init__(self, name: str, kind: str):
        self.name = name
        self.kind = kind

    def validate_command(self, cmd: dict) -> COMMAND: ...


class CommandHandlerCreate(CommandHandler, Generic[STATE, COMMAND, EVENT]):
    def __init__(self, name: str):
        super().__init__(name, "create")

    # todo mettre un autre type qu'optional pour transporter l'erreur
    async def on_command(self, cmd: COMMAND, entityId: str) -> Optional[EVENT]: ...


class CommandHandlerUpdate(CommandHandler, Generic[STATE, COMMAND, EVENT]):
    def __init__(self, name: str):
        super().__init__(name, "update")

    # todo mettre un autre type qu'optional pour transporter l'erreur
    async def on_command(self, cmd: COMMAND, entityId: str, state: STATE) -> Optional[EVENT]: ...
