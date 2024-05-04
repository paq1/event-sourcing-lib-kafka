from typing import TypeVar, Generic

# STATE = TypeVar('STATE')
COMMAND = TypeVar('COMMAND')
# EVENT = TypeVar('EVENT')


class Command(Generic[COMMAND], object):
    def __init__(self, entityId: str, handler_name: str, command: COMMAND):
        self.entityId: str = entityId
        self.handler_name: str = handler_name
        self.command: COMMAND = command
