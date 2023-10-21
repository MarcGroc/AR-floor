from loguru import logger
from src.managers.layout import LayoutManager
from src.paths.pathfinder import Pathfinder
from src.robots.robot import Robot
from src.robots.constants import CRITICAL_BATTERY_LEVEL, LOW_BATTERY_LEVEL, FULL_BATTERY_LEVEL


class PathManager:
    """  Path Manager is responsible for getting path to shelve and path to workstation"""
    def __init__(self) -> None:
        self.pathfinder = Pathfinder

    def check_battery_level(self, robot: Robot, layout: LayoutManager) -> None:
        logger.warning(f"Robot battery level - {round(robot.battery_level, 2)}")
        if robot.battery_level < CRITICAL_BATTERY_LEVEL:
            logger.critical(f"Critical battery level {round(robot.battery_level, 2)}")
            self.get_path_to_charging_station(robot, layout)
        elif robot.battery_level < LOW_BATTERY_LEVEL:
            logger.warning(f"Low battery level {round(robot.battery_level, 2)}")
            self.get_path_to_empty_location(robot, layout)
            self.get_path_to_charging_station(robot, layout)

    def get_path_to_shelve(
        self, target_location: list[int, int], robot: Robot, layout: LayoutManager
    ) -> Robot:
        """Returns Robot with shelve on it"""
        try:
            path_to_destination = self.pathfinder(
                layout.floor, robot.current_location, target_location
            ).get_path_no_load()

            robot.path = path_to_destination
            robot.drive()
            if robot.current_location == target_location:
                layout.floor[target_location[0]][
                    target_location[1]
                ].content.available = False
                layout.floor[target_location[0]][
                    target_location[1]
                ].content.current_location = robot.current_location
                robot.taken_shelve = layout.floor[target_location[0]][
                    target_location[1]
                ].content
                layout.floor[target_location[0]][target_location[1]].content = None
                robot.target_location = None
                return robot
        except Exception as e:
            logger.error(f"Error getting path to Shelve: {e}")
            return robot

    def get_limited_path(
        self, target_location: list[int, int], robot: Robot, layout: LayoutManager
    ) -> Robot:
        self.check_battery_level(robot, layout)
        try:
            path_to_destination = self.pathfinder(
                layout.floor, robot.current_location, target_location
            ).get_path_with_load()
            robot.path = path_to_destination
            robot.drive()
            robot.taken_shelve.current_location = robot.current_location
            self.check_battery_level(robot, layout)
            return robot
        except Exception as e:
            logger.error(f"Error getting limited path: {e}")
            return robot

    def get_path_to_empty_location(self, robot: Robot, layout: LayoutManager) -> Robot:
        try:
            target_location = layout.floor.empty_storing_locations[0]
            path_to_empty_location = self.pathfinder(
                layout.floor, robot.current_location, target_location
            ).get_path_with_load()
            robot.path = path_to_empty_location
            robot.drive()
            if robot.current_location == target_location:
                layout.floor[target_location[0]][
                    target_location[1]
                ].content = robot.taken_shelve
                layout.floor[target_location[0]][
                    target_location[1]
                ].content.available = True
                layout.floor[target_location[0]][
                    target_location[1]
                ].content.current_location = robot.current_location
                robot.taken_shelve = None
                robot.target_location = None
            return robot
        except Exception as e:
            logger.error(f"Error getting path to empty location: {e}")
            return robot

    def get_path_to_charging_station(
        self, robot: Robot, layout: LayoutManager
    ) -> Robot:
        charging_station = layout.get_available_charging_stations()[0]
        try:
            layout.floor[robot.current_location[0]][
                robot.current_location[1]
            ].content = None
            path_to_charging_station = self.pathfinder(
                layout.floor, robot.current_location, charging_station
            ).get_path_no_load()
            robot.path = path_to_charging_station
            robot.drive()
            if robot.current_location == charging_station:
                robot.battery_level = FULL_BATTERY_LEVEL
            return robot
        except Exception as e:
            logger.error(f"Error getting path to charging station: {e}")
            return robot
