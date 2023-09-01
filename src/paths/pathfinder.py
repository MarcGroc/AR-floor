from src.floor.location import Location

NEIGHBOURS = (
    [-1, 0],  # Up
    [1, 0],  # Down
    [0, -1],  # Left
    [0, 1],  # Right
)

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

    def a_star(self) -> list[list[int, int]] | None:
        self.start.g_value = 0
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
                if neighbour in closed_list:
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
        self.starting_location.content.available = False
        return None

    def generate_neighbours(self, starting_location) -> list[Location]:
        return [
            Location(starting_location[0] + i[0], starting_location[1] + i[1])
            for i in NEIGHBOURS
        ]

    def get_manhattan_distance(self, start, end) -> int:
        x = abs(start.coordinates[0] - end.coordinates[0])
        y = abs(start.coordinates[1] - end.coordinates[1])
        return x + y

    def get_path(self, current) -> list[list[int, int]]:
        path = []
        while current is not None:
            path.append(current.coordinates)
            current = current.parent
        return path[::-1]
