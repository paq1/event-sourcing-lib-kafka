from dataclasses import dataclass
from typing import Optional


@dataclass
class CommandApi(object):
    pass


@dataclass
class CommandCreate(CommandApi):
    nom: str
    prenom: str

@dataclass
class CommandUpdate(CommandApi):
    nom: Optional[str]
    prenom: Optional[str]

@dataclass
class State(object):
    pass


@dataclass
class PersonneState(State):
    nom: str
    prenom: str


@dataclass
class Event(object):
    by: str


@dataclass
class CreatePersonneEvent(Event):
    nom: str
    prenom: str

@dataclass
class UpdatePersonneEvent(Event):
    nom: str
    prenom: str
