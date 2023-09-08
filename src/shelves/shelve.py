import uuid

from pydantic import PositiveInt

from src.shelves.bin import Bin
from src.items import Item

MAX_ROWS = 10
MAX_COLUMNS = 6
SHELVE_WIDTH = 100


class Shelve:
    def __init__(self, columns_number: PositiveInt, rows_number: PositiveInt) -> None:
        self.id = uuid.uuid4()
        if columns_number > MAX_COLUMNS or rows_number > MAX_ROWS:
            raise "Invalid dimensions for the shelf"
        self.columns_number = columns_number
        self.rows_number = rows_number
        self.bin_size = SHELVE_WIDTH / self.columns_number
        self.generate_shelf = self.__create_grid()
        self.current_location = None
        self.available = None
        self.contents = None

    def __create_grid(self) -> list[list[Bin]]:
        """Creates shelve with 4 identical sides"""
        side = [
            Bin(row, col, self.bin_size) for col in range(self.rows_number)
            for row in range(self.columns_number)
        ]
        return [side for _ in range(4)]


    def generate(self):
        self.available = True
        self.contents = self.generate_shelf
        return self

    def remove_item(self):
        pass

    def add_item(self, item:Item):
        self.contents[0][0].content.append(item)
        return self.contents[0][0].content

    def get_status(self) -> dict:
        return {
            # "id": self.id,
            "rows": self.rows_number,
            "cols": self.columns_number,
            "current_location": self.current_location,
            "available": self.available,
            "contents": self.contents

        }

    def __repr__(self):
        # todo change to id
        return self.__class__.__name__
