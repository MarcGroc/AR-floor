from random import randrange, choice

from src.floor.layout import ARFloorLayout
from src.floor.location import Location
from src.items.Item import Item
from src.paths.pathfinder import Pathfinder
from src.robots.robot import Robot
from src.shelves.shelve import Shelve
from src.config.states import FloorLocationStates


# todo typing to refcartoring
class MainManager:
    def __init__(self) -> None:
        self.layout = ARFloorLayout()
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
        self.pathfinder = Pathfinder

    def _set_shelves(self) -> list[list[Location]]:
        floor = self.layout.generate
        for row in floor:
            # antipattern refactoring
            for cell, location in enumerate(row):
                if location is None:
                    continue
                if location.purpose == FloorLocationStates.STORING:
                    new_shelve = self.shelve(
                        randrange(1, 6), randrange(1, 10)
                    ).generate()
                    location.content = new_shelve
                    location.content.current_location = location.coordinates
                    self.all_shelves.append(new_shelve)
        return floor

    def _set_robots(self) -> list[list[Location]]:
        floor = self._set_shelves()
        for row in floor:
            for cell, location in enumerate(row):
                if location.purpose == FloorLocationStates.CHARGING:
                    new_robot = self.robot().generate()
                    row[cell].content = new_robot
                    row[cell].content.current_location = row[cell].coordinates
                    self.all_robots.append(new_robot)
        return floor

    def initialize(self) -> list[list[Location]]:
        self.floor = self._set_shelves()
        self.floor = self._set_robots()
        return self.floor

    @property
    def shelves_amount(self) -> int:
        return len(self.all_shelves)

    def get_all_workstations_picking(self):
        return [
            location.coordinates
            for row in self.floor
            for location in row
            if location.purpose == FloorLocationStates.PICKING
        ]

    def get_all_workstations_stowing(self):
        return [
            location.coordinates
            for row in self.floor
            for location in row
            if location.purpose == FloorLocationStates.STOWING
        ]

    @property
    def robots_amount(self) -> int:
        return len(self.all_robots)

    def get_available_robots(self) -> list[Robot]:
        return [robot for robot in self.all_robots if robot.available is True]

    def get_available_shelves(self) -> list[Shelve]:
        return [shelve for shelve in self.all_shelves if shelve.available is True]

    def get_shelve_location(self) -> list[int, int]:
        return choice(self.available_shelves).current_location

    def get_not_taken_location(self) -> list:
        return [
            location.coordinates
            for row in self.floor
            for location in row
            if location.purpose == FloorLocationStates.STORING
            and location.content is None
        ]

    def get_workstations_locations(self):
        return [
            location.coordinates
            for row in self.floor
            for location in row
            if location.purpose == FloorLocationStates.PICKING
        ]

    def get_shelve_path(self) -> Robot:
        """Returns Robot with shelve on it"""
        shelve_location = self.get_shelve_location()
        robot = self.available_robots[0]  # hardcoded for now
        path_to_shelve = self.pathfinder(
            self.floor, robot.current_location, shelve_location
        ).a_star_to_shelve()
        robot.path = path_to_shelve
        robot.drive()
        if robot.current_location == shelve_location:
            self.floor[shelve_location[0]][shelve_location[1]].content.available = False
            self.floor[shelve_location[0]][
                shelve_location[1]
            ].content.current_location = robot.current_location

            robot.taken_shelve = self.floor[shelve_location[0]][
                shelve_location[1]
            ].content
            self.floor[shelve_location[0]][shelve_location[1]].content = None
            robot.target_location = None
            return robot

    def get_workstation_path(self):
        workstation_location = choice(self.workstations_stowing)  # hardcoded for now
        robot = self.get_shelve_path()
        path_to_path = self.pathfinder(
            self.floor, robot.current_location, workstation_location
        ).a_star_to_nearest_on_path_location()
        robot.path = path_to_path
        robot.drive()

        path_to_workstation = self.pathfinder(
            self.floor, robot.current_location, workstation_location
        ).a_star_to_workstation()
        robot.path = path_to_workstation
        robot.drive()
        robot.target_location = None
        robot.taken_shelve.current_location = robot.current_location
        return robot

    def send_to_charging_station(self):
        pass

    def __repr__(self):
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.floor)


i = Item(10, 10, 10, 10, "Item-1")
a = MainManager()
a.available_shelves[0].add_item(i)
print(a.available_shelves[0].contents[0][0].content)
