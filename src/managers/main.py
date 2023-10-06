from loguru import logger

from src.managers.layout import LayoutManager
from src.managers.path import PathManager
from src.robots.robot import Robot


FLOOR_DIMENSION = 30


class MainManager:
    """Main manager responsible for running the system"""

    def __init__(self) -> None:
        self._layout = LayoutManager(FLOOR_DIMENSION)
        self._pathfinder = PathManager()

    def get_shelve(self) -> list[int, int]:
        return self._layout.available_shelves[
            -1
        ].current_location  # hardcoded for tests

    def assign_robot(self) -> Robot:
        return self._layout.available_robots[0]  # hardcoded for tests

    def get_workstation(self) -> list[int, int]:
        return self._layout.workstations_picking[0]  # hardcoded for tests

    def get_available_charging_station(self) -> list[int, int]:
        return self._layout.charging_stations[0]  # hardcoded for tests

    def work(self) -> None:
        logger.info("Starting work - Robot on path to Shelve")
        robot = self._pathfinder.get_path_to_shelve(
            self.get_shelve(), self.assign_robot(), self._layout
        )
        logger.info("Continuing work - Robot on path to Workstation")
        self._pathfinder.get_limited_path(self.get_workstation(), robot, self._layout)
        logger.info("Path completed")

    def __repr__(self):
        return f"{self._layout.floor}"
