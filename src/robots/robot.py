import uuid
from typing import Optional

from loguru import logger

from src.config.directions import Directions
from src.items.item import Item
from src.shelves.shelve import Shelve
from src.robots.constants import FULL_BATTERY_LEVEL

class Robot:
    """Robot class"""

    def __init__(self) -> None:
        self._id: uuid.UUID = uuid.uuid4()
        self.current_location: list[int, int] = []
        self.battery_level: int = FULL_BATTERY_LEVEL
        self.available: bool = None  # noqa
        self.heading: Directions = None  # noqa
        self.path: list[list[int, int]] = []
        self.target_location: list[int, int] = []
        self.taken_shelve: Optional[Shelve] = None

    def drive(self):
        self.available = False
        if not self.path:
            logger.error(f"Path is empty {self.path}")
            return

        self.target_location = self.path[-1]

        while self.current_location != self.target_location:
            self.turn()
            self.current_location = self.path[0]
            self.path.pop(0)

    def turn(self):
        if self.path[0][0] == self.current_location[0] - 1:
            self.heading = Directions.NORTH
            self.update_battery()
        elif self.path[0][0] == self.current_location[0] + 1:
            self.heading = Directions.SOUTH
            self.update_battery()
        elif self.path[0][1] == self.current_location[1] + 1:
            self.heading = Directions.EAST
            self.update_battery()
        elif self.path[0][1] == self.current_location[1] - 1:
            self.heading = Directions.WEST
            self.update_battery()
        else:
            raise ValueError("Invalid next_location")

    def update_battery(self):
        if self.taken_shelve is None:
            self.battery_level -= 0.1
        else:
            self.battery_level -= 0.5

    def rotate_shelve(self, item: Item, workstation_side):
        if self.taken_shelve is None:
            return

        side_to_rotate = self._find_side_to_rotate(item)
        if side_to_rotate:
            self._rotate_side_if_needed(side_to_rotate, workstation_side)

    def _find_side_to_rotate(self, item: Item):
        for side in self.taken_shelve.content:
            for bin in side.content:
                if item in bin.content:
                    return side
        return None

    def _rotate_side_if_needed(self, side, workstation_side):
        item_side_direction = side.side_direction
        if workstation_side == item_side_direction:
            logger.info(f"No need to rotate")
        else:
            side.side_direction = workstation_side
            logger.info(
                f"Rotate shelf from {item_side_direction} to {workstation_side}"
            )

    def initialize(self):
        self.available = True
        self.heading = Directions.NORTH
        return self

    def get_status(self):
        return {
            "id": self._id,
            "available": self.available,
            "current_location": self.current_location,
            "heading": self.heading,
            "battery": self.battery_level,
            "target_location": self.target_location,
            "taken_shelve": self.taken_shelve,
        }

    def __repr__(self):
        return self.__class__.__name__
