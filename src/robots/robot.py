import uuid

from src.config.directions import Directions


class Robot:
    def __init__(self):
        self.__id = uuid.uuid4()
        self.current_location = []  # 2d location
        self.target_location = []  # 2d location
        self.battery_level = 100
        self.available = None
        self.heading = None

    def drive_forward(self):
        pass

    def turn_(self):
        # right or left
        pass

    def stop(self):
        # if on target location, unable to move forward, need to turn, rotate shelve, pullup/down shelve
        pass

    def head_direction(self):
        # change on turn
        return self.heading

    def pull_up_shelve(self):
        # if on target location, available and stop
        pass

    def rotate_shelve(self):
        # robot rotates shelve only to right :)
        pass

    def pull_down_shelve(self):
        # drive to target location, stop, available true
        pass

    def generate(self):
        self.available = True
        self.heading = "N"
        return self

    def get_status(self):
        return {
            "id": self.__id,
            "available": self.available,
            "heading": self.heading,
            "battery": self.battery_level,
        }

    def __repr__(self):
        return self.__class__.__name__
