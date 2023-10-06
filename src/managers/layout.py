from loguru import logger
from random import randrange

from src.config.states import LocationStates
from src.floor.layout import FloorLayout
from src.floor.location import Location
from src.robots.robot import Robot
from src.shelves.shelve import Shelve


class LayoutManager:
    """ Layout Manager initializes floor layout, robots, shelves and holds information about them """
    def __init__(self, floor_dimension: int) -> None:
        self.__validate_dimension(floor_dimension)
        self.layout: FloorLayout = FloorLayout(floor_dimension)
        self.robot = Robot
        self.shelve = Shelve
        self.all_shelves = []
        self.all_robots = []
        self.floor = self.initialize()
        self.empty_storing_locations = self.get_not_taken_location()
        self.available_robots = self.get_available_robots()
        self.available_shelves = self.get_available_shelves()
        self.workstations_picking = self.get_all_workstations_picking()
        self.workstations_stowing = self.get_all_workstations_stowing()
        self.charging_stations = self.get_available_charging_stations()

    def __validate_dimension(self, floor_dimension):
        if floor_dimension < 30:
            raise ValueError("Floor dimension must be at least 30")

    def get_cell_purpose(self, coordinates: list[int, int]) -> LocationStates:
        return self.layout.floor_layout[coordinates[0]][coordinates[1]].purpose

    @property
    def robots_amount(self) -> int:
        return len(self.all_robots)

    @property
    def shelves_amount(self) -> int:
        return len(self.all_shelves)

    def get_available_robots(self) -> list[Robot]:
        return [robot for robot in self.all_robots if robot.available is True]

    def get_available_shelves(self) -> list[Shelve]:
        return [shelve for shelve in self.all_shelves if shelve.available is True]

    def get_all_workstations_picking(self) -> list[list[int, int]]:
        return [
            location.coordinates
            for row in self.layout.floor_layout
            for location in row
            if location.purpose == LocationStates.PICKING
        ]

    def get_all_workstations_stowing(self) -> list[list[int, int]]:
        return [
            location.coordinates
            for row in self.layout.floor_layout
            for location in row
            if location.purpose == LocationStates.STOWING
        ]

    def get_available_charging_stations(self) -> list[list[int, int]]:
        return [
            location.coordinates
            for row in self.layout.floor_layout
            for location in row
            if location.purpose == LocationStates.CHARGING
        ]

    def get_not_taken_location(self) -> list[list[int, int]]:
        return [
            location.coordinates
            for row in self.layout.floor_layout
            for location in row
            if location.purpose == LocationStates.STORING and location.content is None
        ]

    def _init_shelve(self, location):
        if location is not None and location.purpose == LocationStates.STORING:
            new_shelve = self.shelve(randrange(1, 6), randrange(1, 10)).initialize()
            location.content = new_shelve
            location.content.current_location = location.coordinates
            self.all_shelves.append(new_shelve)

    def _set_shelves(self) -> list[list[Location]]:
        floor = self.layout.floor_layout
        for row in floor:
            for cell, location in enumerate(row):
                self._init_shelve(location)
        return floor

    def _set_robots(self) -> list[list[Location]]:
        floor = self._set_shelves()
        for row in floor:
            for cell, location in enumerate(row):
                if location.purpose == LocationStates.CHARGING:
                    new_robot = self.robot().initialize()
                    row[cell].content = new_robot
                    row[cell].content.current_location = row[cell].coordinates
                    self.all_robots.append(new_robot)
        return floor

    def initialize(self) -> list[list[Location]]:
        self.floor = self._set_shelves()
        self.floor = self._set_robots()
        logger.info("Floor initialized")
        return self.floor
