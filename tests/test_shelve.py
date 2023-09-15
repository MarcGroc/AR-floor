import pytest

from src.config.directions import Directions
from src.items.Item import Item
from src.shelves.bin import Bin
from src.shelves.side import Side


class TestBin:

    def test_bin_creation_positive_size(self):
        size = 5
        test_bin = Bin(size)
        assert test_bin.width == size
        assert test_bin.length == size
        assert test_bin.height == size
        assert test_bin.content == []

    def test_bin_creation_zero_size(self):
        size = 0
        with pytest.raises(ValueError):
            Bin(size)

    def test_bin_creation_negative_size(self):
        size = -1
        with pytest.raises(ValueError):
            Bin(size)


class TestSide:

    @pytest.fixture
    def test_side(self):
        bins = [Bin(10) for _ in range(3)]
        return Side(bins, Directions.NORTH)

    def test_add_item(self, test_side):
        item = Item(5, 5, 5, 2, "Test Item")
        test_side.add_item(item, 0)
        assert item in test_side.content[0].content

    def test_remove_item(self, test_side):
        item = Item(5, 5, 5, 2, "Test Item")
        test_side.add_item(item, 0)
        test_side.remove_item(item, 0)
        assert item not in test_side.content[0].content

    def test_add_item_too_large(self, test_side):
        item = Item(15, 5, 5, 2, "Large Item")
        with pytest.raises(Exception):
            test_side.add_item(item, 0)

    def test_remove_item_not_in_bin(self, test_side):
        item = Item(5, 5, 5, 2, "Missing Item")
        with pytest.raises(Exception):
            test_side.remove_item(item, 0)
