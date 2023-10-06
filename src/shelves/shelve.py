import uuid

from loguru import logger
from pydantic import PositiveInt

from src.config.directions import Directions
from src.shelves.bin import Bin
from src.items import Item
from src.shelves.side import Side

MAX_ROWS = 10
MAX_COLUMNS = 6
SHELVE_WIDTH = 100


class Shelve:
    """ Represents a shelve """
    def __init__(self, columns_number: PositiveInt, rows_number: PositiveInt) -> None:
        self.id: uuid.UUID = uuid.uuid4()
        self.columns_number = columns_number
        self.rows_number = rows_number
        self.__validate_dimensions()
        self.bin_size: float = SHELVE_WIDTH / self.columns_number
        self.initialize_shelf = self.__create_sides()
        self.current_location = None
        self.available = None
        self.content = None

    def __validate_dimensions(self):
        if self.columns_number > MAX_COLUMNS or self.rows_number > MAX_ROWS:
            raise ValueError(
                f"Invalid dimensions for the shelf. Max columns: {MAX_COLUMNS}, Max rows: {MAX_ROWS}"
            )

    def __create_sides(self) -> list[Side]:
        """Creates shelve with 4 identical sides"""
        bins = [
            Bin(self.bin_size) for _ in range(self.rows_number * self.columns_number)
        ]
        return [Side(bins, direction) for direction in Directions]

    def add_item(self, item: Item, side: Directions, bin_index: int) -> None:
        shelve_side = next(_ for _ in self.initialize_shelf if _.side_direction == side)
        shelve_side.add_item(item, bin_index)
        logger.info(f"Added item {item} to {side} bin {bin_index}")


    def remove_item(self, item: Item, side: Directions, bin_index: int) -> None:
        shelve_side = next(_ for _ in self.initialize_shelf if _.side_direction == side)
        shelve_side.remove_item(item, bin_index)
        logger.info(f"Removed item {item} from {side} bin {bin_index}")

    def initialize(self):
        self.available = True
        self.content = self.__create_sides()
        return self

    def get_status(self) -> dict:
        return {
            "id": self.id,
            "rows": self.rows_number,
            "cols": self.columns_number,
            "current_location": self.current_location,
            "available": self.available,
            "bin_size": self.bin_size,
            "content": self.content,
        }

    def __repr__(self):
        return self.__class__.__name__
