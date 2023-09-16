import pytest

from src.floor.location import Location
from src.floor.layout import FloorLayout

class TestLocation:

    @pytest.fixture
    def location(self):
        return Location(0,0)

    def test_initialize(self, location):
        assert isinstance(location, Location)
        assert location.coordinates == [0,0]


class TestFloor:

    @pytest.fixture
    def layout(self):
        layout = FloorLayout()
        return layout.initialize

    def test_initialize(self, layout):
        assert len(layout) > 0


