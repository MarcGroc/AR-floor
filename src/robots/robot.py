import uuid

from src.config.directions import Directions
from src.items.Item import Item


class Robot:
    def __init__(self) -> None:
        self._id = uuid.uuid4()
        self.current_location = []
        self.battery_level = 100
        self.available = None
        self.heading = None
        self.path = []
        self.target_location = []
        self.taken_shelve = None

    def drive(self):
        self.available = False
        self.target_location = self.path[-1]

        while self.current_location != self.target_location:
            self.turn()
            self.current_location = self.path[0]
            self.path.pop(0)

    def turn(self):
        if self.path[0][0] == self.current_location[0] - 1:
            self.heading = Directions.NORTH
            self.battery_status()
        elif self.path[0][0] == self.current_location[0] + 1:
            self.heading = Directions.SOUTH
            self.battery_status()
        elif self.path[0][1] == self.current_location[1] + 1:
            self.heading = Directions.EAST
            self.battery_status()
        elif self.path[0][1] == self.current_location[1] - 1:
            self.heading = Directions.WEST
            self.battery_status()

    def battery_status(self):
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
                        print(f"No need to rotate")
                        continue
                    else:
                        side.side_direction = workstation_side
                        print(
                            f"Rotate shelf from {item_side_direction} to {workstation_side}"
                        )
                    return 1

    def generate(self):
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
