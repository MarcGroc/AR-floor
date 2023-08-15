from src.floor.layout import ARFloorLayout
from src.robots.robot import ARRobot
from src.shelves.shelve import ARShelve

class ContextManager:
    def __init__(self):
        self.layout = ARFloorLayout()
        self.robot = ARRobot() # dośmyslnie ustić robty na połnoc
        self.shelf = ARShelve()
        self.initialize()

    def initialize(self):
        # todo stworzyć layout, dodać shelves do layout i roboty
        ...


