import uuid
from typing import Optional

from src.config.states import LocationStates
from src.robots.robot import Robot
from src.shelves.shelve import Shelve


class Location:
    def __init__(
        self,
        row,
        col,
    ) -> None:
        self.id: uuid.UUID = uuid.uuid4()
        self.coordinates: list[int,int] = [row, col]
        self.purpose: LocationStates = None
        self.content: Optional[Shelve, Robot, None] = None

        # A* algorithm
        self.f_value: int = 0
        self.g_value: int = 0
        self.parent: list[int, int] = None

    def __eq__(self, other):
        return self.coordinates == other.coordinates

    def __repr__(self):
        return str(self.purpose.value)


    def get_status(self) -> dict:
        return {
            "coordinates": self.coordinates,
            "purpose": self.purpose,
            "content": self.content,
        }
