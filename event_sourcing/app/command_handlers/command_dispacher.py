from typing import Generic, TypeVar, Optional, Tuple

import logging

from event_sourcing.app.command_handlers.command_handler import CommandHandler, CommandHandlerCreate, \
    CommandHandlerUpdate
from event_sourcing.models.command import Command

COMMAND = TypeVar('COMMAND')
STATE = TypeVar('STATE')
EVENT = TypeVar('EVENT')

class CommandDispatcher(Generic[STATE, COMMAND, EVENT]):
    logger = logging.getLogger(f"{__name__}#CommandDispatcher")

    def __init__(self):
        self.command_handlers: list[CommandHandler[STATE, COMMAND, EVENT]] = []

    def with_handler(self, handler: CommandHandler):
        self.command_handlers.append(handler)
        return self

    async def exec(self, command: Command, state: Optional[STATE]) -> Optional[Tuple[EVENT, int]]:
        handlers = [handler for handler in self.command_handlers if handler.name == command.handler_name]
        if len(handlers) > 0:
            handler: CommandHandler[STATE, COMMAND, EVENT] = handlers[0]
            if handler.kind == "create":
                self.logger.debug("traitement d'un handler de creation")
                create_handler: CommandHandlerCreate[STATE, COMMAND, EVENT] = handler
                cmd_parsed: COMMAND = create_handler.validate_command(command.data)
                return await create_handler.on_command(cmd_parsed, command.entityId), 201
            else:
                self.logger.debug("traitement d'un handler de maj")
                update_handler: CommandHandlerUpdate[STATE, COMMAND, EVENT] = handler
                cmd_parsed: COMMAND = update_handler.validate_command(command.data)
                return await update_handler.on_command(cmd_parsed, command.entityId, state), 200
