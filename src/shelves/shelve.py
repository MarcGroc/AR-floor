import uuid

from pydantic import PositiveInt, field_validator


class ARShelve:
    def __init__(self, columns_number: PositiveInt, rows_number: PositiveInt):
        self.id = uuid.uuid4()
        self.columns_number = columns_number #max 6
        self.rows_number = rows_number # max 10
        self.grid = self.create_grid()

    def create_grid(self):
        side = [
            [_ for _ in range(self.rows_number)] for _ in range(self.columns_number)
        ]
        shelf = [side for _ in range(4)]
        return shelf

    def is_bin_empty(self):
        # check if shelf bin is empty or its space to shelve item
        pass

    def stow_item(self):
        # put item into bin
        pass

    def pick_item(self):
        # take item from bin
        pass

    def __str__(self):
        return f"ARShelve: {self.id}, Grid {self.grid}"

