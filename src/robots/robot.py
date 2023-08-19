import uuid


class ARRobot:
    def __init__(self):
        self.id = uuid.uuid4()
        self.current_location = []
        self.target_location = None
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
        # north if in charging station
        pass

    def pull_up_shelve(self):
        # if on target location, available and stop
        pass

    def rotate_shelve(self):
        # robot rotates shelve only to right :)
        pass

    def pull_down_shelve(self):
        # drive to target location, stop, available true
        pass

    def detect_obstacles(self):
        pass

    def generate(self, row, col):
        # to refactor
        self.available = True
        self.heading = 'N'
        self.current_location = [col, row]
        return self.available, self.heading, self.current_location
