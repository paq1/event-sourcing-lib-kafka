class CreateFromDict:

    @staticmethod
    def from_toto(d: dict): return "toto"
    @staticmethod
    def from_dict(d: dict) -> 'CreateFromDict': ...
