from random import choice


from src.managers.layout import LayoutManager
from src.managers.path import PathManager
from src.paths.pathfinder import Pathfinder
from src.robots.robot import Robot


FLOOR_DIMENSION = 30


class MainManager:
    def __init__(self) -> None:
        self.layout = LayoutManager(FLOOR_DIMENSION)
        self.pathfinder = PathManager()

    def get_shelve(self) -> list[int, int]:
        return self.layout.available_shelves[-1].current_location

    def assign_robot(self) -> Robot:
        return self.layout.available_robots[0]

    def get_workstation(self) -> list[int, int]:
        return self.layout.workstations_picking[0]

    def get_available_charging_station(self) -> list[int, int]:
        return self.layout.charging_stations[0]

    def work(self):
        robot = self.pathfinder.get_shelve_path(self.get_shelve(), self.assign_robot(), self.layout)
        self.pathfinder.get_limited_path(
            self.get_workstation(), robot , self.layout
        )
        print("Path completed")

    def __repr__(self):
        return "\n".join(
            " ".join(str(cell) for cell in row) for row in self.layout.floor
        )
