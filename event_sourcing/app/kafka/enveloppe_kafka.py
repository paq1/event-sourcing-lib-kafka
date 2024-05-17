class SubjectResultKafka(object):
    def __init__(self, key: str, content: dict[str, str]):
        self.key = key
        self.content = content

    def __str__(self):
        return f"[{self.key}]: {self.content}"