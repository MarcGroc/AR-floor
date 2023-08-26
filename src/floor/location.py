import uuid
from typing import Optional, Union

from src.config.states import FloorLocationStates
from src.robots.robot import Robot
from src.shelves.shelve import Shelve


class Location:
    def __init__(
        self,
        purpose: FloorLocationStates,
        content: Optional[Union["Robot", "Shelve", None]],
    ) -> None:
        self.__id = uuid.uuid4()
        self.purpose = purpose
        self.content = content

    @property
    def get_id(self):
        return self.__id

    def get_status(self) -> dict:
        return {
            "purpose": self.purpose.name,
            "content": self.content,
        }

    def __str__(self):
        return str(self.purpose.name)
