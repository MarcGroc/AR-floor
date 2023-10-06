import pytest

from src.config.directions import Directions
from src.items.Item import Item
from src.shelves.bin import Bin
from src.shelves.shelve import Shelve, SHELVE_WIDTH
from src.shelves.side import Side


class TestBin:
    def test_bin_creation_positive_size(self):
        size = 1
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

    @pytest.fixture
    def item(self):
        return Item(5, 5, 5, 2, "Test Item")

    def test_add_item(self, item, test_side):
        test_side.add_item(item, 0)
        assert item in test_side.content[0].content

    def test_remove_item(self, item, test_side):
        test_side.add_item(item, 0)
        test_side.remove_item(item, 0)
        assert item not in test_side.content[0].content

    def test_add_item_too_large(self, test_side):
        item = Item(51, 51, 51, 51, "Big-item")
        with pytest.raises(Exception):
            test_side.add_item(item, 0)

    def test_remove_item_not_in_bin(self, item, test_side):
        with pytest.raises(Exception):
            test_side.remove_item(item, 0)


class TestShelve:
    @pytest.fixture
    def item(self):
        return Item(20, 20, 20, 20, "test-item")

    @pytest.fixture
    def shelve(self):
        shelve = Shelve(5, 3)
        shelve.initialize()
        return shelve

    @pytest.fixture
    def side(self):
        return  Directions.NORTH

    @pytest.fixture
    def bin_index(self):
        return 0

    def test_create_shelve_with_valid_dimensions(self, shelve):
        columns_number = 5
        rows_number = 3
        assert isinstance(shelve, Shelve)
        assert shelve.columns_number == columns_number
        assert shelve.rows_number == rows_number
        assert shelve.bin_size == SHELVE_WIDTH / columns_number

    def test_create_shelve_with_invalid_dimensions(self):
        columns_number = 12
        rows_number = 8
        with pytest.raises(ValueError):
            Shelve(columns_number, rows_number)

    def test_add_remove_item_to_bin_in_shelve(self, item, bin_index, side, shelve):
        shelve.add_item(item, side, bin_index)
        shelve_side = next(s for s in shelve.initialize_shelf if s.side_direction == side)
        assert item in shelve_side.content[bin_index].content

        shelve.remove_item(item, side, bin_index)
        assert item not in shelve_side.content[bin_index].content


    def test_add_item_to_bin_with_incorrect_size(self, side, bin_index, shelve):
        item = Item(51, 51, 51, 51, "Big-item")
        with pytest.raises(Exception):
            shelve.add_item(item, side, bin_index)

    def test_remove_missing_item(self, item, bin_index, side, shelve):
        with pytest.raises(Exception):
            shelve.remove_item(item, side, bin_index)
