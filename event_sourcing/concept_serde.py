from dataclasses import dataclass
from typing import Optional

import marshmallow_dataclass


@dataclass
class Adresse(object):
    rue: str
    pays: str


@dataclass
class SimpleObject(object):
    _kind: Optional[str]
    name: str
    adresse: Adresse


def run() -> None:
    data = '{"_kind": "urn:api:test:simple-object","name": "Pierre", "adresse": { "rue": "12 rue du pré", "pays": "fr"}}'
    simple_obj_schema = marshmallow_dataclass.class_schema(SimpleObject)()
    obj = simple_obj_schema.loads(data)
    print(obj)
    # wip https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object
