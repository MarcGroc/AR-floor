import uuid

from src.config.directions import Directions


class Robot:
    def __init__(self):
        self.__id = uuid.uuid4()
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
        elif self.path[0][0] == self.current_location[0] + 1:
            self.heading = Directions.SOUTH
        elif self.path[0][1] == self.current_location[1] + 1:
            self.heading = Directions.EAST
        elif self.path[0][1] == self.current_location[1] - 1:
            self.heading = Directions.WEST

    def rotate_shelve(self):
        # if self.heading != self.taken_shelve
        pass

    def generate(self):
        self.available = True
        self.heading = Directions.NORTH
        return self

    def get_status(self):
        return {
            # "id": self.__id,
            "available": self.available,
            "current_location": self.current_location,
            "heading": self.heading,
            "battery": self.battery_level,
            "target_location": self.target_location,
            "taken_shelve": self.taken_shelve
        }
    def __repr__(self):
        return self.__class__.__name__
