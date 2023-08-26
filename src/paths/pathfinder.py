from src.config.directions import Directions

GRID = (
    [-1, -1],
    [-1, 0],
    [-1, +1],
    [0, -1],
    [0, 0],
    [0, +1],
    [+1, -1],
    [+1, 0],
    [+1, +1],
)


class Pathfinder:
    def __init__(self, floor, start, stop):
        self.grid = floor
        self.start = start
        self.stop = stop

    def detect_obstacles(self):
        current_position = self.start
        return current_position, self.stop
