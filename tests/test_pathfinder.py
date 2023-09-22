import pytest
from pytest_mock import mocker

from src.paths.pathfinder import Pathfinder, BlockedCantMove
from src.floor.location import Location
from src.robots.robot import Robot
from src.config.neighbours import Neighbours
from src.shelves.shelve import Shelve
from src.floor.layout import FloorLayout

SIZE_LAYOUT = 30


class TestPathfinder:

    @pytest.fixture
    def layout(self):
        layout = FloorLayout(SIZE_LAYOUT)
        return layout.floor_layout

    def test_get_path_no_load(self, layout):
        starting_location = [15, 15]
        target_location = [0, 8]
        pathfinder = Pathfinder(layout, starting_location, target_location)

        path = pathfinder.get_path_no_load()
        assert path is not False
        assert path[-1] == target_location

    def test_get_path_with_load(self, layout):
        starting_location = [15, 15]
        target_location = [29, 12]
        pathfinder = Pathfinder(layout, starting_location, target_location)
    
        path = pathfinder.get_path_with_load()
        assert path is not False
        assert path[-1] == target_location

    # def test_block_path_with_robot(self, layout):
    #     starting_location = [14, 14]
    #     target_location = [0, 8]
    #     pathfinder = Pathfinder(layout, starting_location, target_location)
    #
    #     path = pathfinder.get_path_no_load()
    #     assert path is False
    #
    #
    # def test_block_path_with_shelve(self, layout):
    #     starting_location = [12, 12]
    #     target_location = [0, 8]
    #     pathfinder = Pathfinder(layout, starting_location, target_location)
    #
    #     path = pathfinder.get_path_with_load()
    #     assert path is False