import uuid

from pydantic import PositiveInt, field_validator


class ARShelve:
    def __init__(self, columns_number: PositiveInt, rows_number: PositiveInt):
        self.id = uuid.uuid4()
        self.columns_number = columns_number  # max 6
        self.rows_number = rows_number  # max 10
        self.generate_shelf = self.create_grid()
        self.current_location = self.set_current_location()
    def create_grid(self):
        side = [
            [_ for _ in range(self.rows_number)] for _ in range(self.columns_number)
        ]
        shelf = [side for _ in range(4)]
        return shelf

    def generate(self):
        return self.generate_shelf
    def set_current_location(self):
        pass

    def check_contents(self):
        # check if shelf bin is empty or its space to shelve items, check weight of items
        pass

    def take_item(self):
        # ake item form bin and update weight and space left in the bin
        pass

    def add_item(self):
        # add item to bin and update weight and space left in the bin
        pass

    def display_items(self):
        # for visualization
        pass

    def get_status(self):
        # id, location, stock
        pass

    def __str__(self):
        return f"ARShelve: {self.id}, Grid {self.generate}"
