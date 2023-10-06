import pytest

from src.config.states import LocationStates
from src.managers.layout import LayoutManager
from src.robots.robot import Robot
from src.shelves.shelve import Shelve

LAYOUT_DIMENSION = 30
class TestLayoutManager:
    @pytest.fixture
    def layout_manager(self):
        return LayoutManager(LAYOUT_DIMENSION)
    
    
    def test_invalid_floor_dimension(self):
        with pytest.raises(ValueError):
            LayoutManager(20)
    
    
    def test_valid_floor_dimension(self, layout_manager):
        assert layout_manager is not None
    
    
    def test_robot_amount(self, layout_manager):
        assert isinstance(layout_manager.robots_amount, int)
    
    
    def test_shelves_amount(self, layout_manager):
        assert isinstance(layout_manager.shelves_amount, int)
    
    
    def test_get_cell_purpose(self, layout_manager):
        assert layout_manager.get_cell_purpose([0, 0]) in LocationStates
    
    
    def test_get_available_robots(self, layout_manager):
        robots = layout_manager.get_available_robots()
        assert all(isinstance(robot, Robot) for robot in robots)
    
    
    def test_get_available_shelves(self, layout_manager):
        shelves = layout_manager.get_available_shelves()
        assert all(isinstance(shelve, Shelve) for shelve in shelves)
    
    
    def test_get_all_workstations_picking(self, layout_manager):
        stations = layout_manager.get_all_workstations_picking()
        assert all(isinstance(coord, list) for coord in stations)
    
    
    def test_get_all_workstations_stowing(self, layout_manager):
        stations = layout_manager.get_all_workstations_stowing()
        assert all(isinstance(coord, list) for coord in stations)
    
    
    def test_get_available_charging_stations(self, layout_manager):
        stations = layout_manager.get_available_charging_stations()
        assert all(isinstance(coord, list) for coord in stations)
    
    
    def test_get_not_taken_location(self, layout_manager):
        locations = layout_manager.get_not_taken_location()
        assert all(isinstance(coord, list) for coord in locations)
    

