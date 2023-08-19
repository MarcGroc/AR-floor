import time
from random import randrange

from src.floor.layout import ARFloorLayout
from src.robots.robot import ARRobot
from src.shelves.shelve import ARShelve
from src.config.states import FloorLocationStates


class ContextManager:
    def __init__(self):
        #  refactoring
        self.__charging_point = FloorLocationStates.CHARGING.value
        self.layout = ARFloorLayout()
        self.robot = ARRobot  # list of robots
        self.shelve = ARShelve  # list of shelves
        self.shelves_amount = self.count_shelves()
        self.floor = self.initialize()

    def __set_shelves(self):
        floor = self.layout.generate()
        for row in floor:
            for cell in row:
                if cell == 1:
                    row[cell] = self.shelve(randrange(1, 5), randrange(1, 10)).generate()
                    # row[cell] = "Y"
        return floor

    def count_shelves(self):
        return sum(cell == 1 for row in self.layout.generate() for cell in row)

    def __set_robots(self):
        floor = self.__set_shelves()
        for row in floor[-3:]:
            for cell in range(len(row) - 3, len(row)):
                row[cell] = self.robot().generate(cell, cell)
        return floor

    def initialize(self):
        self.floor = self.__set_shelves()
        self.floor = self.__set_robots()
        return self.floor

    def get_robot_id(self):
        pass

    def assign_task(self):
        # iterate over list of robots if robot is available assign for task
        pass

    def send_to_charging_station(self):
        # while self.robot.battery_level > 10:
        #     time.sleep(60)
        #     self.robot.battery_level -= 1
        # if self.robot.battery_level <= 10:
        #     if self.available:
        #         # drive to charging station
        #         pass
        #     else:
        #         # drive to nearest shelve location and then to charging station
        #         self.get_empty_shelve_location()
        pass

    def get_station_location(self):
        # if pull_up_shelve
        pass

    def get_shelve_location(self):
        # for task
        pass

    def get_not_taken_location(self):
        # get empty location of inner floor if there is no prediction for items stored in shelve for next 5 mins,
        # or battery level is low
        pass

    def __str__(self):
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.floor)


a = ContextManager()
for i in a.floor:
    print(i)

