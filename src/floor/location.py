import uuid
from typing import Optional, Union

from src.config.states import FloorLocationStates
from src.robots.robot import Robot
from src.shelves.shelve import Shelve


class Location:
    def __init__(
        self, row, col,
    ) -> None:
        self.__id = uuid.uuid4()
        self.coordinates = [row, col]
        self.purpose = None
        self.content = None
        # A* algorithm
        self.f_value = float('inf')
        self.g_value = float('inf')
        self.parent = None

    @property
    def get_id(self):
        return self.__id

    def get_status(self) -> dict:
        return {
            "coordinates": self.coordinates,
            "purpose": self.purpose,
            "content": self.content,
        }

