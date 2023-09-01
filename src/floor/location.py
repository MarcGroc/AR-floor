import uuid


class Location:
    def __init__(
        self,
        row,
        col,
    ) -> None:
        self.__id = uuid.uuid4()
        self.coordinates = [row, col]
        self.purpose = None
        self.content = None

        # A* algorithm
        self.f_value = 0
        self.g_value = 0
        self.parent = None

    def __eq__(self, other):
        return self.coordinates == other.coordinates

    @property
    def get_id(self):
        return self.__id

    def get_status(self) -> dict:
        return {
            "coordinates": self.coordinates,
            "purpose": self.purpose,
            "content": self.content,
        }
