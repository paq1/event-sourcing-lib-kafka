from dataclasses import dataclass
from typing import Optional

from event_sourcing.models.can_transform_into_dict import CanTransformIntoDict


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
class Event(CanTransformIntoDict):
    by: str


@dataclass
class CreatePersonneEvent(Event, CanTransformIntoDict):
    nom: str
    prenom: str

    def transform_into_dict(self) -> dict:
        return {
            "nom": self.nom,
            "prenom": self.prenom,
        }

@dataclass
class UpdatePersonneEvent(Event, CanTransformIntoDict):
    nom: str
    prenom: str

    def transform_into_dict(self) -> dict:
        return {
            "nom": self.nom,
            "prenom": self.prenom,
        }
