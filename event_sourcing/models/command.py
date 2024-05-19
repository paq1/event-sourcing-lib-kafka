from dataclasses import dataclass
from typing import TypeVar, Generic

# STATE = TypeVar('STATE')
COMMAND = TypeVar('COMMAND')
# EVENT = TypeVar('EVENT')


@dataclass
class Command(object):
    entityId: str
    handler_name: str
    data: dict
