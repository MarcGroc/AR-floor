import pytest

from src.managers.layout import LayoutManager
from src.managers.path import PathManager
from src.robots.robot import (
    Robot,
    CRITICAL_BATTERY_LEVEL,
    LOW_BATTERY_LEVEL,
    FULL_BATTERY_LEVEL,
)
from src.managers.main import FLOOR_DIMENSION


class TestPathManager:
    @pytest.fixture
    def path_manager(self):
        return PathManager()


    @pytest.fixture
    def layout_manager(self):
        return LayoutManager(FLOOR_DIMENSION)


    @pytest.fixture
    def robot(self):
        return Robot()

    def test_check_battery_level_critical(self,path_manager, robot, layout_manager):
        robot.battery_level = CRITICAL_BATTERY_LEVEL - 1
        path_manager.check_battery_level(robot, layout_manager)

    def test_check_battery_level_low(self, path_manager, robot, layout_manager):
        robot.battery_level = LOW_BATTERY_LEVEL - 1
        path_manager.check_battery_level(robot, layout_manager)

    def test_get_path_to_shelve(self,path_manager, robot, layout_manager):
        target = [0, 0]
        result = path_manager.get_path_to_shelve(target, robot, layout_manager)
        assert result is not None

    def test_get_limited_path(self, path_manager, robot, layout_manager):
        target = [0, 0]
        result = path_manager.get_limited_path(target, robot, layout_manager)
        assert result is not None

    def test_get_path_to_empty_location(self, path_manager, robot, layout_manager):
        result = path_manager.get_path_to_empty_location(robot, layout_manager)
        assert result is not None

    def test_get_path_to_charging_station(self, path_manager, robot, layout_manager):
        result = path_manager.get_path_to_charging_station(robot, layout_manager)
        assert result is not None
        assert result.battery_level == FULL_BATTERY_LEVEL
