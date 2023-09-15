import uuid

from pydantic import PositiveInt

from src.config.directions import Directions
from src.shelves.bin import Bin
from src.items import Item
from src.shelves.side import Side

MAX_ROWS = 10
MAX_COLUMNS = 6
SHELVE_WIDTH = 100


class Shelve:
    def __init__(self, columns_number: PositiveInt, rows_number: PositiveInt) -> None:
        self.id = uuid.uuid4()
        if columns_number > MAX_COLUMNS or rows_number > MAX_ROWS:
            raise ValueError("Invalid dimensions for the shelf")
        self.columns_number = columns_number
        self.rows_number = rows_number
        self.bin_size = SHELVE_WIDTH / self.columns_number
        self.generate_shelf = self.__create_shelve()
        self.current_location = None
        self.available = None
        self.content = None

    def __create_shelve(self) -> list[Side]:
        """Creates shelve with 4 identical sides"""
        bins = [
            Bin(self.bin_size) for _ in range(self.rows_number * self.columns_number)
        ]
        return [Side(bins, direction) for direction in Directions]

    def add_item(self, item: Item, side: Directions, bin_index: int) -> None:
        shelve_side = next(direction for direction in self.generate_shelf if direction.side_direction == side)
        shelve_side.add_item(item, bin_index)

    def remove_item(self, item: Item, side: Directions, bin_index: int) -> None:
        shelve_side = next(_ for _ in self.generate_shelf if _.side_direction == side)
        shelve_side.remove_item(item, bin_index)

    def generate(self):
        self.available = True
        self.content = self.generate_shelf
        return self

    def get_status(self) -> dict:
        return {
            # "id": self.id,
            "rows": self.rows_number,
            "cols": self.columns_number,
            "current_location": self.current_location,
            "available": self.available,
            "bin_size": self.bin_size,
            "content": self.content,
        }

    def __repr__(self):
        return self.__class__.__name__
