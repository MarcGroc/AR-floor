from src.config.directions import Directions

from src.floor.location import Location

# NEIGHBOURS = (
#     [-1, -1],
#     [-1, 0],
#     [-1, +1],
#     [0, -1],
#     [0, 0],
#     [0, +1],
#     [+1, -1],
#     [+1, 0],
#     [+1, +1],
# )

NEIGHBOURS = (
    [-1, 0],  # Up
    [1, 0],  # Down
    [0, -1],  # Left
    [0, 1],  # Right
)


class Pathfinder:
    """A* algorith implementation"""
    def __init__(self, floor, starting_location, target_location):
        self.floor = floor
        self.starting_location = starting_location
        self.target_location = target_location

        # A* algorithm implementation
        self.neighbours = self.generate_neighbours()
        self.start = Location(starting_location[0], starting_location[1])
        self.end = Location(target_location[0], target_location[1])
        self.open_list = [self.start]
        self.closed_list = []
        self.current_location = None



    def generate_neighbours(self):
        return [
            [self.starting_location[0] + i[0], self.starting_location[1] + i[1]]
            for i in NEIGHBOURS
        ]

    def get_available_locations(self):
        return [
            [self.floor[neighbour[0]][neighbour[1]].coordinates]
            for neighbour in self.neighbours
            if self.floor[neighbour[0]][neighbour[1]].content is None
        ]

    def get_manhattan_distance(self):
        x = abs(self.start.coordinates[0] - self.end.coordinates[0])
        y = abs(self.start.coordinates[1] - self.end.coordinates[1])
        return x+y
    def a_star(self):
        self.start.g_value = 0
        self.start.f_value = self.start.g_value + self.get_manhattan_distance()

        return self.start.f_value
