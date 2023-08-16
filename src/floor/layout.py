from pydantic import PositiveInt, NonNegativeInt
from typing import List

from src.config.states import FloorLocationStates
from src.config.areas import FloorAreas


class ARFloorLayout:
    """Creates floor layout and assign integer  to each field, there are states for floor location:"""

    def __init__(self):
        self.__x_axis: PositiveInt = 30
        self.__y_axis: PositiveInt = 30
        self.outer = FloorAreas.OUTER_FLOOR.value
        self.inner = FloorAreas.INNER_FLOOR.value
        self.first_aisle = FloorAreas.FIRST_AISLE.value
        self.aisle_gap = FloorAreas.AISLE_GAP.value
        self.waiting = FloorLocationStates.WAITING.value
        self.first_waiting_line = FloorAreas.FIRST_WAITING_LINE.value
        self.on_path = FloorLocationStates.ON_PATH.value
        self.not_taken = FloorLocationStates.NOT_TAKEN.value
        self.taken = FloorLocationStates.TAKEN.value
        self.picking = FloorLocationStates.PICKING.value
        self.stowing = FloorLocationStates.STOWING.value
        self.floor_layout = self.set_cells_for_paths()

    def create_floor_layout(self) -> List[List[NonNegativeInt]]:
        return [
            [self.not_taken for _ in range(self.__x_axis)] for _ in range(self.__y_axis)
        ]

    def set_cells_for_shelf_storing(self):
        layout_with_paths = self.create_floor_layout()
        layout = layout_with_paths

        for row in layout[self.inner : -self.inner]:
            for cell, value in enumerate(row):
                if (
                    self.inner <= cell < self.__y_axis - self.inner
                    and value != self.on_path
                ):
                    row[cell] = self.taken
        return layout

    def set_cells_for_waiting(self):
        layout_with_storing = self.set_cells_for_shelf_storing()
        layout = layout_with_storing

        for row in layout[self.first_waiting_line : self.outer]:
            # top horizontal
            for cell in range(len(row)):
                if (
                    self.first_waiting_line
                    <= cell
                    < self.__x_axis - self.first_waiting_line
                ):
                    row[cell] = self.waiting

        for row in layout[self.__x_axis - self.outer : -self.first_waiting_line]:
            # bottom horizontal
            for cell in range(len(row)):
                if (
                    self.first_waiting_line
                    <= cell
                    < self.__x_axis - self.first_waiting_line
                ):
                    row[cell] = self.waiting

        for row in layout[self.first_waiting_line : -self.first_waiting_line]:
            # vertical
            for cell in range(len(row)):
                if (
                    self.first_waiting_line <= cell < self.outer
                    and cell != self.on_path
                    or self.__y_axis - self.outer
                    <= cell
                    < self.__y_axis - self.first_waiting_line
                    and cell != self.on_path
                ):
                    row[cell] = self.waiting

        return layout

    def set_cells_for_picking_and_stowing(self):
        layout_with_waiting = self.set_cells_for_waiting()
        layout = layout_with_waiting

        for cell in range(6, len(layout[0]) - 4, 8):
            # horizontal rows picking
            layout[0][cell] = self.picking
            layout[-1][cell] = self.picking
        for cell in range(10, len(layout[0]) - 4, 8):
            # horizontal rows stowing
            layout[0][cell] = self.stowing
            layout[-1][cell] = self.stowing

        for cell in range(4, len(layout) - 4, 8):
            # left and right columns picking
            layout[cell][0] = self.picking
            layout[cell][-1] = self.picking
        for cell in range(8, len(layout) - 4, 8):
            # left and right columns stowing
            layout[cell][0] = self.stowing
            layout[cell][-1] = self.stowing

        return layout

    def set_cells_for_paths(self) -> List[List[NonNegativeInt]]:
        clean_floor = self.set_cells_for_picking_and_stowing()
        layout = clean_floor
        for row in layout[self.outer : -self.outer]:
            # vertical left and right
            for cell in range(len(row)):
                if (
                    self.outer <= cell < self.inner
                    or self.__y_axis - self.inner <= cell < self.__y_axis - self.outer
                ):
                    row[cell] = self.on_path
        for row in layout[self.outer : self.inner]:
            # horizontal top
            for cell in range(len(row)):
                if self.inner <= cell <= self.__x_axis - self.inner:
                    row[cell] = self.on_path

        for row in layout[self.__x_axis - self.inner : self.__x_axis - self.outer]:
            # horizontal bottom
            for i in range(len(row)):
                if self.inner <= i < self.__y_axis - self.inner:
                    row[i] = self.on_path

        for row in layout[
            self.first_aisle : self.__x_axis - self.inner : self.aisle_gap
        ]:
            # aisles horizontal
            for cell in range(len(row)):
                row[cell] = self.on_path
        for row in layout:
            # aisles vertical
            for cell in range(
                self.first_aisle, self.__y_axis - self.inner, self.aisle_gap
            ):
                row[cell] = self.on_path

        return layout

    def __repr__(self):
        return "\n".join(
            " ".join(str(cell) for cell in row) for row in self.floor_layout
        )


a = ARFloorLayout()
print(a)
