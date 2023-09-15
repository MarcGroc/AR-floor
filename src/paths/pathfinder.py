from src.config.states import FloorLocationStates
from src.floor.location import Location
from src.robots.robot import Robot
from src.config.neighbours import Neighbours
from src.shelves.shelve import Shelve

COST = 1


class Pathfinder:
    """A* algorith implementation"""

    def __init__(self, floor, starting_location, target_location) -> None:
        self.floor = floor
        self.starting_location = starting_location
        self.target_location = target_location

        # A* algorithm implementation
        self.neighbours = self.generate_neighbours(self.starting_location)
        self.start = Location(starting_location[0], starting_location[1])
        self.end = Location(target_location[0], target_location[1])

    def a_star_to_shelve(self) -> list[list[int, int]] | None:
        self.start.f_value = self.start.g_value + self.get_manhattan_distance(
            self.start, self.end
        )
        open_list = [self.start]
        closed_list = []

        while len(open_list) > 0:
            current = min(open_list, key=lambda node: node.f_value)
            if current.coordinates == self.end.coordinates:
                return self.get_path(current)

            open_list.remove(current)
            closed_list.append(current)
            neighbours = self.generate_neighbours(current.coordinates)

            # todo if blocked to refactor
            if all(isinstance(neighbour.content, Robot) for neighbour in neighbours):
                print("cant move, waiting....")
                # move to the end of available robots list? or sleep
                return None

            for neighbour in neighbours:
                if neighbour in closed_list or isinstance(neighbour.content, Robot):
                    continue

                temp_g_value = neighbour.g_value + COST

                if neighbour not in open_list:
                    open_list.append(neighbour)
                elif temp_g_value >= neighbour.g_value:
                    continue
                neighbour.parent = current
                neighbour.g_value = temp_g_value
                neighbour.f_value = neighbour.g_value + self.get_manhattan_distance(
                    neighbour, self.end
                )
        return None

    def a_star_to_nearest_on_path_location(self):
        self.start.f_value = self.start.g_value + self.get_manhattan_distance(
            self.start, self.end
        )
        open_list = [self.start]
        closed_list = []

        while len(open_list) > 0:
            current = min(open_list, key=lambda node: node.f_value)
            if current.purpose == FloorLocationStates.ON_PATH:
                return self.get_path(current)

            open_list.remove(current)
            closed_list.append(current)
            neighbours = self.generate_neighbours(current.coordinates)

            for neighbour in neighbours:
                if neighbour in closed_list or isinstance(neighbour.content, Robot):
                    continue

                temp_g_value = neighbour.g_value + COST

                if neighbour not in open_list:
                    open_list.append(neighbour)
                elif temp_g_value >= neighbour.g_value:
                    continue
                neighbour.parent = current
                neighbour.g_value = temp_g_value
                neighbour.f_value = neighbour.g_value + self.get_manhattan_distance(
                    neighbour, self.end
                )
        return None

    def a_star_to_workstation(self) -> list[list[int, int]] | None:
        self.start.f_value = self.start.g_value + self.get_manhattan_distance(
            self.start, self.end
        )
        open_list = [self.start]
        closed_list = []

        while len(open_list) > 0:
            current = min(open_list, key=lambda node: node.f_value)
            if current.coordinates == self.end.coordinates:
                return self.get_path(current)

            open_list.remove(current)
            closed_list.append(current)
            neighbours = self.generate_neighbours(current.coordinates)

            for neighbour in neighbours:
                if neighbour in closed_list or neighbour.content in [Robot, Shelve]:
                    continue

                temp_g_value = neighbour.g_value + COST

                if neighbour not in open_list:
                    open_list.append(neighbour)
                elif temp_g_value >= neighbour.g_value:
                    continue
                neighbour.parent = current
                neighbour.g_value = temp_g_value
                neighbour.f_value = neighbour.g_value + self.get_manhattan_distance(
                    neighbour, self.end
                )
        return None

    def generate_neighbours(self, starting_location) -> list[Location]:
        # todo to refactoring
        neighbours = []
        for i in Neighbours:
            x = starting_location[0] + i.value[0]
            y = starting_location[1] + i.value[1]

            if 0 <= x < len(self.floor) and 0 <= y < len(self.floor[0]):
                neighbours.append(self.floor[x][y])
        return neighbours

    def get_manhattan_distance(self, start, end) -> int:
        x = abs(start.coordinates[0] - end.coordinates[0])
        y = abs(start.coordinates[1] - end.coordinates[1])
        return x + y

    def get_path(self, current) -> list[list[int, int]]:
        path = []
        while current is not None:
            path.append(current.coordinates)
            current = current.parent
        path = path[::-1]
        return path[1:]
