import pytest

from src.config.directions import Directions
from src.items.Item import Item
from src.robots.robot import Robot


class TestRobot:
    @pytest.fixture
    def robot(self):
        robot = Robot().initialize()
        robot.current_location = [0, 0]
        return robot

    def test_initialize(self, robot):
        assert isinstance(robot, Robot)
        assert robot.available is True
        assert robot.heading == Directions.NORTH
        assert robot.battery_level == 100

    def test_drive(self, robot):
        robot.path = [[0, 1], [0, 2], [0, 3]]
        robot.drive()
        assert robot.available is False
        assert robot.current_location == [0, 3]
        assert robot.battery_level < 100

    def test_turn(self, robot):
        robot.path = [[0, 1]]
        robot.turn()
        assert robot.heading == Directions.EAST
        robot.path = [[1, 0]]
        robot.turn()
        assert robot.heading == Directions.SOUTH

    def test_rotate_shelf_to_workstation_side(self, mocker):
        robot = Robot()
        item = Item(1.0, 1.0, 1.0, 1.0, "item")
        workstation_side = Directions.EAST
        robot.taken_shelve = mocker.Mock()
        robot.taken_shelve.content = [mocker.Mock()]
        robot.taken_shelve.content[0].content = [mocker.Mock()]
        robot.taken_shelve.content[0].content[0].content = [item]
        robot.rotate_shelve(item, workstation_side)
        assert robot.taken_shelve.content[0].side_direction == workstation_side
