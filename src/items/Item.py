from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Item:
    # id: uuid4()
    width: float
    length: float
    height: float
    weight: float
    name: str

    def __repr__(self):
        return self.name