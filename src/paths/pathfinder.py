from loguru import logger

from src.floor.location import Location
from src.robots.robot import Robot
from src.config.neighbours import Neighbours
from src.shelves.shelve import Shelve

COST = 1


class Pathfinder:
    """A* algorith implementation"""

    def __init__(
        self,
        floor: list[list[Location]],
        starting_location: list[int, int],
        target_location: list[int, int],
    ) -> None:
        self.floor = floor
        self.starting_location = starting_location
        self.target_location = target_location

        # A* algorithm implementation
        self.start = Location(starting_location[0], starting_location[1])
        self.end = Location(target_location[0], target_location[1])

    def get_path_no_load(self) -> list[list[int, int]] | None:
        self.start.f_value = self.calculate_f_value(self.start, self.end)
        open_list, closed_list = [self.start], []

        while len(open_list) > 0:
            current = min(open_list, key=lambda node: node.f_value)
            if current.coordinates == self.end.coordinates:
                return self.get_path(current)

            self.process_node(current, open_list, closed_list, obstacle_type=(Robot,))

        return None

    def get_path_with_load(self) -> list[list[int, int]] | None:
        self.start.f_value = self.calculate_f_value(self.start, self.end)
        open_list, closed_list = [self.start], []

        while len(open_list) > 0:
            current = min(open_list, key=lambda node: node.f_value)
            if current.coordinates == self.end.coordinates:
                return self.get_path(current)

            self.process_node(
                current, open_list, closed_list, obstacle_type=(Robot, Shelve)
            )

        return None

    def process_node(
        self, current, open_list, closed_list, obstacle_type=(Robot,)
    ) -> None:
        open_list.remove(current)
        closed_list.append(current)
        neighbours = self.generate_neighbours(current.coordinates)
        # self.check_for_blockage(neighbours)
        for neighbour in neighbours:
            if neighbour in closed_list or isinstance(neighbour.content, obstacle_type):
                continue

            temp_g_value = neighbour.g_value + COST

            if neighbour not in open_list:
                open_list.append(neighbour)
            elif temp_g_value >= neighbour.g_value:
                continue
            self.update_node(neighbour, current, temp_g_value)

    def check_for_blockage(self, neighbours): # This will be refactored, not implemented yet
        count_robot = 0
        count_shelve = 0
        count_empty = 0

        for neighbour in neighbours:
            if isinstance(neighbour.content, Robot):
                count_robot += 1
            elif isinstance(neighbour.content, Shelve):
                count_shelve += 1
            else:
                count_empty += 1

        if count_robot == len(neighbours):
            logger.error("Blocked by robots")
            # raise BlockedCantMove("Blocked by robots")
        elif count_shelve == len(neighbours):
            logger.error("Blocked by shelves")
            # raise BlockedCantMove("Blocked by shelves")

        return 1

    def update_node(self, node, parent, temp_g_value) -> None:
        node.parent = parent
        node.g_value = temp_g_value
        node.f_value = node.g_value + self.get_manhattan_distance(node, self.end)

    def calculate_f_value(self, start, end) -> int:
        return start.g_value + self.get_manhattan_distance(start, end)

    def generate_neighbours(self, starting_location) -> list[Location]:
        return [
            self.floor[starting_location[0] + neighbour.value[0]][
                starting_location[1] + neighbour.value[1]
            ]
            for neighbour in Neighbours
            if 0 <= starting_location[0] + neighbour.value[0] < len(self.floor)
            and 0 <= starting_location[1] + neighbour.value[1] < len(self.floor[0])
        ]

    def get_manhattan_distance(self, start, end) -> int:
        return abs(start.coordinates[0] - end.coordinates[0]) + abs(
            start.coordinates[1] - end.coordinates[1]
        )

    def get_path(self, current) -> list[list[int, int]]:
        path = []
        while current is not None:
            path.append(current.coordinates)
            current = current.parent
        path = path[::-1]
        return path[1:]
