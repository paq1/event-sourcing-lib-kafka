from threading import Thread
from typing import TypeVar, Generic

import asyncio

from event_sourcing.app.listeners.commands_listener import CommandsListener

COMMAND = TypeVar('COMMAND')
STATE = TypeVar('STATE')
EVENT = TypeVar('EVENT')


class ThreadListenerCommands(Thread, Generic[STATE, COMMAND, EVENT]):
    def __init__(self, commands_listener: CommandsListener[STATE, COMMAND, EVENT]):
        super().__init__()
        self.commands_listener = commands_listener

    def run(self):
        self.commands_listener.run()
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # loop.create_task(self.commands_listener.run())

    def stop(self):
        self.commands_listener.stop()
