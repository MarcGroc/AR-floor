import uuid

from pydantic import PositiveInt

MAX_ROWS = 10
MAX_COLUMNS = 6


class Shelve:
    def __init__(self, columns_number: PositiveInt, rows_number: PositiveInt) -> None:
        self.id = uuid.uuid4()
        if columns_number > MAX_COLUMNS or rows_number > MAX_ROWS:
            raise "Invalid dimensions for the shelf"
        self.columns_number = columns_number
        self.rows_number = rows_number
        self.generate_shelf = self.__create_grid()
        self.available = None
        self.contents = self.generate_shelf

    def __create_grid(self) -> list[list[list[int]]]:
        """Creates shelve with 4 identical sides"""
        side = [
            [_ for _ in range(self.rows_number)] for _ in range(self.columns_number)
        ]
        shelf = [side for _ in range(4)]
        return shelf

    def generate(self):
        self.available = True
        return self

    def check_contents(self):
        # check if shelf bin is empty or its space to shelve items, check weight of items
        pass

    def take_item(self):
        # ake item form bin and update weight and space left in the bin
        pass

    def add_item(self):
        pass

    def display_items(self):
        # for visualization
        pass

    def get_status(self) -> dict:
        return {"id": self.id, "available": self.available, "rows": self.rows_number, "cols": self.columns_number}

    def __repr__(self):
        return self.__class__.__name__
