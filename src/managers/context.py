from src.floor.layout import ARFloorLayout
from src.robots.robot import ARRobot
from src.shelves.shelve import ARShelve
from src.config.states import FloorLocationStates


class ContextManager:
    def __init__(self):
        self.layout = ARFloorLayout()
        self.robot = ARRobot()  # dośmyslnie ustić robty na połnoc
        self.shelf = ARShelve(3, 7) #todo generator półek
        self.initialize()
        self.shelfs_amount = 0


    # def count_shelfs(self):
    #     for row in self.layout:
    #         for cell in row:
    #             if cell == 1:
    #                 self.shelfs_amount += 1
    def initialize(self):
        # todo stworzyć layout, dodać shelves do layout i roboty
        ...

a = ContextManager()
