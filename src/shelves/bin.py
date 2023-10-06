import uuid
from uuid import uuid4


class Bin:
    """ Represents a bin in shelf side """
    def __init__(self, size) -> None:
        if size <= 0:
            raise ValueError("Size must be greater than zero.")
        self.id: uuid.UUID = uuid4()
        self.width: int = size
        self.length: int = self.width
        self.height: int = self.width
        self.content: list = []

    def get_status(self) -> dict:
        return vars(self)

    def __repr__(self):
        return self.__class__.__name__
