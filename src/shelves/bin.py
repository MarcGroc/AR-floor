from uuid import uuid4


class Bin:
    def __init__(self, size) -> None:
        self.__id = uuid4()
        self.width = size
        self.length = self.width
        self.height = self.width
        self.content = []

    def get_status(self) -> dict:
        return vars(self)

    def __repr__(self):
        return self.__class__.__name__
