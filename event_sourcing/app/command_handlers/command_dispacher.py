from typing import Generic, TypeVar, Self

COMMAND = TypeVar('COMMAND')
STATE = TypeVar('STATE')
EVENT = TypeVar('EVENT')


class CommandHandler(object, Generic[COMMAND, STATE, EVENT]):
    def __init__(self, name: str, kind: str):
        self.name = name
        self.kind = kind


class CommandHandlerCreate(CommandHandler, Generic[COMMAND, STATE, EVENT]):
    def __init__(self, name: str):
        super().__init__(name, "create")

    async def on_command(self, cmd: COMMAND, entityId: str) -> EVENT: ...


class CommandHandlerUpdate(CommandHandler, Generic[COMMAND, STATE, EVENT]):
    def __init__(self, name: str):
        super().__init__(name, "update")

    async def on_command(self, cmd: COMMAND, entityId: str, state: STATE) -> EVENT: ...


class CommandDispacher(Generic[COMMAND, STATE, EVENT]):
    def __init__(self):
        self.command_handlers: list[CommandHandler[COMMAND, STATE, EVENT]] = []

    def with_handler(self, handler: CommandHandler) -> Self:
        self.command_handlers.append(handler)
        return self

    async def exec(self, command_name: str, command: COMMAND, state: STATE = None) -> EVENT:
        handlers = [handler for handler in self.command_handlers if handler.name == command_name]
        if len(handlers) > 0:
            handler = handlers[0]
            if handler.kind == "create":
                create_handler: CommandHandlerCreate[COMMAND, STATE, EVENT] = handler
                return await create_handler.on_command(command, "xxxx")
            else:
                # mkdmkd fixme pas le droit :)
                return None
