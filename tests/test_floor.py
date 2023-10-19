import pytest

from src.config.areas import FloorAreas
from src.config.directions import Directions
from src.config.states import LocationStates
from src.floor.location import Location
from src.floor.layout import FloorLayout

SIZE_LAYOUT = 30


class TestLocation:
    @pytest.fixture
    def location(self):
        return Location(0, 0)

    def test_initialize(self, location):
        assert isinstance(location, Location)
        assert location.coordinates == [0, 0]


class TestFloor:
    @pytest.fixture
    def layout(self):
        layout = FloorLayout(SIZE_LAYOUT)
        return layout

    def test_initialize(self, layout):
        assert len(layout.floor_layout) == SIZE_LAYOUT
        assert len(layout.floor_layout[0]) == SIZE_LAYOUT

    def test_assign_purpose_to_cells(self, layout):
        layout._assign_purpose_to_cells(0, 2, 0, 2, LocationStates.STORING)
        for row in layout.floor_layout[0:2]:
            for cell in row[0:2]:
                assert cell.purpose == LocationStates.STORING

    def test_assigns_storing_to_cells_within_range(self, layout):
        layout._initialize_shelve_storing_areas()
        for row in range(FloorAreas.INNER_FLOOR.value, -FloorAreas.INNER_FLOOR.value):
            for col in range(
                FloorAreas.INNER_FLOOR.value,
                layout._y_axis - FloorAreas.INNER_FLOOR.value,
            ):
                assert layout.floor_layout[row][col].purpose == LocationStates.STORING

    def test_initialize_waiting_areas_top_horizontal(self, layout):

        layout._initialize_waiting_areas()

        for row in range(FloorAreas.INITIAL_WAITING_LINE.value, FloorAreas.OUTER_FLOOR.value):
            for col in range(
                FloorAreas.INITIAL_WAITING_LINE.value,
                SIZE_LAYOUT - FloorAreas.INITIAL_WAITING_LINE.value,
            ):
                assert layout.floor_layout[row][col].purpose == LocationStates.WAITING

    def test_initialize_picking_and_stowing_areas(self, layout):

        for row in [0, -1]:
            for col in range(0, layout._x_axis):
                if layout.floor_layout[row][col].purpose == LocationStates.PICKING:
                    assert layout.floor_layout[row][col].heading in [
                        Directions.NORTH,
                        Directions.SOUTH,
                    ]
    
        for row in [0, -1]:
            for col in range(0, layout._x_axis):
                if layout.floor_layout[row][col].purpose == LocationStates.STOWING:
                    assert layout.floor_layout[row][col].heading in [
                        Directions.NORTH,
                        Directions.SOUTH,
                    ]
