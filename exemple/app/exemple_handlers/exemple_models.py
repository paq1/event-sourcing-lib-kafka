from dataclasses import dataclass


@dataclass
class CommandApi(object):
    pass


@dataclass
class CommandCreate(CommandApi):
    nom: str
    prenom: str


@dataclass
class State(object):
    pass


@dataclass
class CreateState(State):
    nom: str
    prenom: str


@dataclass
class Event(object):
    by: str


@dataclass
class CreateEvent(Event):
    nom: str
    prenom: str
