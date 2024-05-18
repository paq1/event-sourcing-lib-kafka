from event_sourcing.models.from_dict import CreateFromDict
from event_sourcing.models.has_schema import HasSchema


class CommandTest(HasSchema, CreateFromDict):
    ...


class CreerBobCommand(CommandTest):
    def __init__(self, nom: str, prenom: str):
        self.nom = nom
        self.prenom = prenom

    def schema(self) -> dict:
        return {
            "nom": self.nom,
            "prenom": self.prenom
        }

    @staticmethod
    def from_dict(schema: dict):
        return CreerBobCommand(schema["nom"], schema["prenom"])
