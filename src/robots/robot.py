import uuid
from typing import Optional

from loguru import logger

from src.config.directions import Directions
from src.items.Item import Item
from src.shelves.shelve import Shelve

FULL_BATTERY_LEVEL = 100
LOW_BATTERY_LEVEL = 20
CRITICAL_BATTERY_LEVEL = 15


class Robot:
    """ Robot class """
    def __init__(self) -> None:
        self._id: uuid.UUID = uuid.uuid4()
        self.current_location: list[int, int] = []
        self.battery_level: int = FULL_BATTERY_LEVEL
        self.available: bool = None
        self.heading: Directions = None
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
        self.battery_level -= 0.5

    def rotate_shelve(self, item: Item, workstation_side):
        if self.taken_shelve is None:
            return None

        for side in self.taken_shelve.content:
            for bin_index, bin in enumerate(side.content):
                if item in bin.content:
                    item_side_direction = side.side_direction
                    if workstation_side == item_side_direction:
                        logger.info(f"No need to rotate")
                        continue
                    else:
                        side.side_direction = workstation_side
                        logger.info(
                            f"Rotate shelf from {item_side_direction} to {workstation_side}"
                        )
                    return 1

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
