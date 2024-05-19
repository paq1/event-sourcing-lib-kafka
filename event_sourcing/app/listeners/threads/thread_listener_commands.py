from threading import Thread
from typing import TypeVar, Generic

import asyncio

from event_sourcing.app.listeners.commands_listener import CommandsListener

COMMAND = TypeVar('COMMAND')
STATE = TypeVar('STATE')
EVENT = TypeVar('EVENT')


class ThreadListenerCommandsHandler(Generic[STATE, COMMAND, EVENT]):
    def __init__(self, commands_listener: CommandsListener[STATE, COMMAND, EVENT]):
        self.commands_listener = commands_listener
        self.__thread = Thread(target=self.thread_callback,)

    def thread_callback(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.commands_listener.run())
        loop.close()

    def start(self):
        self.__thread.start()

    def stop(self):
        self.commands_listener.stop()
        self.__thread.join()
