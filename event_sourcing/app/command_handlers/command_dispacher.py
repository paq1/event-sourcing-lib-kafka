from typing import Generic, TypeVar, Optional

import logging

from event_sourcing.models.command import Command

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

    # todo mettre un type qu'optional pour transporter l'erreur
    async def on_command(self, cmd: COMMAND, entityId: str) -> Optional[EVENT]: ...


class CommandHandlerUpdate(CommandHandler, Generic[STATE, COMMAND, EVENT]):
    def __init__(self, name: str):
        super().__init__(name, "update")

    # todo mettre un type qu'optional pour transporter l'erreur
    async def on_command(self, cmd: COMMAND, entityId: str, state: STATE) -> Optional[EVENT]: ...


class CommandDispatcher(Generic[STATE, COMMAND, EVENT]):
    logger = logging.getLogger(f"{__name__}#CommandDispatcher")

    def __init__(self):
        self.command_handlers: list[CommandHandler[STATE, COMMAND, EVENT]] = []

    def with_handler(self, handler: CommandHandler):
        self.command_handlers.append(handler)
        return self

    async def exec(self, command: Command, state: Optional[STATE]) -> Optional[EVENT]:
        handlers = [handler for handler in self.command_handlers if handler.name == command.handler_name]
        if len(handlers) > 0:
            handler: CommandHandler[STATE, COMMAND, EVENT] = handlers[0]
            if handler.kind == "create":
                self.logger.debug("traitement d'un handler de creation")
                create_handler: CommandHandlerCreate[STATE, COMMAND, EVENT] = handler
                cmd_parsed: COMMAND = create_handler.validate_command(command.data)
                return await create_handler.on_command(cmd_parsed, command.entityId)
            else:
                self.logger.debug("traitement d'un handler de maj")
                update_handler: CommandHandlerUpdate[STATE, COMMAND, EVENT] = handler
                cmd_parsed: COMMAND = update_handler.validate_command(command.data)
                return await update_handler.on_command(cmd_parsed, command.entityId, state)
