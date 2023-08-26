from random import randrange

from src.floor.layout import ARFloorLayout
from src.paths.pathfinder import Pathfinder
from src.robots.robot import Robot
from src.shelves.shelve import Shelve
from src.config.states import FloorLocationStates


class MainManager:
    def __init__(self) -> None:
        self.layout = ARFloorLayout()
        self.robot = Robot  # for initialization
        self.shelve = Shelve  # as above
        self.all_shelves = []  # list of all shelves on the floor
        self.all_robots = []  # list of all robots on the floor
        self.floor = self.initialize()
        self.available_locations = self.get_not_taken_location()  # empty areas where shelve can be stored
        self.available_robots = self.get_available_robots()  # without task assigned
        self.available_shelves = self.get_available_shelves()  # without task assigned
        self.path = Pathfinder

    def _set_shelves(self) -> list[list[Shelve]]:
        floor = self.layout.generate
        for row in floor:
            for cell, location in enumerate(row):
                if location is None:
                    continue
                if location.purpose.value == FloorLocationStates.STORING.value:
                    new_shelve = self.shelve(
                        randrange(1, 6), randrange(1, 10)
                    ).generate()
                    location.content = new_shelve
                    self.all_shelves.append(new_shelve)
        return floor

    def _set_robots(self):
        floor = self._set_shelves()
        # todo move charging station to middle of grid
        for row in floor[-3:]:
            for cell in range(len(row) - 3, len(row)):
                new_robot = self.robot().generate()
                row[cell].content = new_robot # fix typehint
                self.all_robots.append(new_robot)
        return floor

    def initialize(self):
        self.floor = self._set_shelves()
        self.floor = self._set_robots()
        return self.floor

    @property
    def shelves_amount(self):
        return len(self.all_shelves)

    @property
    def robots_amount(self):
        return len(self.all_robots)

    def get_available_robots(self):
        return [robot for robot in self.all_robots if robot.available is True]

    def get_available_shelves(self):
        return [shelve for shelve in self.all_shelves if shelve.available is True]

    def get_shelve_location(self):
        # for now hardcoded
        return self.all_shelves[60].current_location

    def assign_task(self):
        # get item id,
        # find in which bin item is stored, check if shelve is available,
        # get shelve location, get nearest available robot to shelve location,
        # send robot with shelve to location
        shelve_location = self.get_shelve_location()
        robot = self.available_robots[0]
        path = self.path(self.floor, robot.current_location, shelve_location)
        return path.detect_obstacles()

    def get_station_location(self):
        # if pull_up_shelve
        pass

    def get_not_taken_location(self):
        # todo assign empty locations
        # empty_locations = []
        # for row in self.floor:
        #     for cell, location in enumerate(row):
        #         if location.content is None:
        #             empty_locations.append(location)
        pass


    # def send_to_charging_station(self):
    #     while self.robot.battery_level > 10:
    #         time.sleep(60)
    #         self.robot.battery_level -= 1
    #     if self.robot.battery_level <= 10:
    #         if self.available:
    #             # drive to charging station
    #             pass
    #         else:
    #             # drive to nearest shelve location and then to charging station
    #             self.get_empty_shelve_location()
    #     pass

    def __repr__(self):
        return "\n".join("".join(str(cell) for cell in row) for row in self.floor)


a = MainManager()
print(a)
print(a.floor[-1][-1].content)
print(a.floor[-10][-10].content)
