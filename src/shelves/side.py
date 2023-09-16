import uuid
from uuid import uuid4


from src.config.directions import Directions
from src.items.Item import Item
from src.shelves.bin import Bin


class Side:
    def __init__(self, bins: list[Bin], direction: Directions) -> None:
        self.id: uuid.UUID = uuid4()
        self.content = bins
        self.side_direction = direction

    def add_item(self, item: Item, bin_index: int) -> None:
        if item.width > self.content[bin_index].width or item.length > self.content[bin_index].length or item.height > self.content[bin_index].height:
            raise Exception("Do not add this item, incorrect size")
        self.content[bin_index].content.append(item)

    def remove_item(self, item: Item, bin_index: int) -> None:
        try:
            self.content[bin_index].content.remove(item)
        except ValueError:
            raise "Item not in Bin"

    def get_status(self) -> dict:
        return vars(self)

    def __repr__(self):
        return str(self.side_direction)
