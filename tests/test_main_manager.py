import pytest

from src.managers.layout import LayoutManager
from src.managers.main import MainManager
from src.robots.robot import Robot


class TestMainManager:
    @pytest.fixture
    def manager(self):
        return MainManager()

    @pytest.fixture
    def robot(self):
        return Robot()

    @pytest.fixture
    def layout(self):
        return LayoutManager(30)

    def test_get_workstation(self, manager, layout):
        assert manager.get_workstation() is not None

    def test_get_shelve(self, manager, layout):
        assert manager.get_shelve() is not None

    def test_assign_robot(self, manager, robot, layout):
        assert manager.assign_robot() is not None

    def test_get_available_charging_station(self, manager, layout):
        assert manager.get_available_charging_station() is not None

    def test_work(self, manager, robot):
        manager.work()
