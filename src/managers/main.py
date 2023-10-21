from random import choice
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
        return choice(self._layout.available_shelves).current_location

    def assign_robot(self) -> Robot:
        return self._layout.available_robots[0]

    def get_workstation(self) -> list[int, int]:
        return choice(self._layout.workstations_picking)

    def get_available_charging_station(self) -> list[int, int]:
        return self._layout.charging_stations[0]

    def work(self) -> None:
        """This is "visualization" of system in action"""
        logger.info("Starting work - Robot on path to Shelve")
        robot = self.assign_robot()
        logger.info(f"Robot current location {robot.current_location}")
        logger.info("Starting work - Robot on path to Shelve")
        shelve = self.get_shelve()
        logger.info(f"Shelve location {shelve}")
        path = self._pathfinder.get_path_to_shelve(shelve, robot, self._layout)
        logger.info(f"Robot current location {robot.current_location}")
        logger.info("Continuing work - Robot on path to Workstation")
        workstation = self.get_workstation()
        logger.info(f"Workstation location {workstation}")
        self._pathfinder.get_limited_path(workstation, path, self._layout)
        logger.info(f"Robot current location {robot.current_location}")
        logger.success("Work completed")

    def __repr__(self):
        return f"{self._layout.floor}"
