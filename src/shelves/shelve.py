import uuid


class ARShelve:
    def __init__(self, columns_number: int, rows_number: int):
        self.id = uuid.uuid4()
        self.__columns_number = columns_number
        self.__rows_number = rows_number
        self.shelve_grid = self.create_grid()

    def create_grid(self):
        pass

    def __str__(self):
        return f"ARShelve: {self.id}, Grid {self.shelve_grid}"
