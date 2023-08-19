from pydantic import PositiveInt, NonNegativeInt
from typing import List

from src.config.states import FloorLocationStates
from src.config.areas import FloorAreas

__all__ = ["ARFloorLayout"]


class ARFloorLayout:
    """Creates floor layout and assign integer  to each field, there are states for floor location:"""

    def __init__(self):
        self.__x_axis: PositiveInt = 30
        self.__y_axis: PositiveInt = 30
        self.__outer = FloorAreas.OUTER_FLOOR.value
        self.__inner = FloorAreas.INNER_FLOOR.value
        self.__first_aisle = FloorAreas.FIRST_AISLE.value
        self.__aisle_gap = FloorAreas.AISLE_GAP.value
        self.__waiting = FloorLocationStates.WAITING.value
        self.__first_waiting_line = FloorAreas.FIRST_WAITING_LINE.value
        self.__on_path = FloorLocationStates.ON_PATH.value
        self.__not_taken = FloorLocationStates.NOT_TAKEN.value
        self.__taken = FloorLocationStates.TAKEN.value
        self.__picking = FloorLocationStates.PICKING.value
        self.__stowing = FloorLocationStates.STOWING.value
        self.__charging = FloorLocationStates.CHARGING.value
        self.__floor_layout = self.__set_charging_area()

    def __create_floor_layout(self) -> List[List[NonNegativeInt]]:
        return [
            [self.__not_taken for _ in range(self.__x_axis)]
            for _ in range(self.__y_axis)
        ]

    def __set_cells_for_shelve_storing(self):
        """
        Sets the cells for shelve storing on the floor layout.

        :return: The updated floor layout with cells set for shelve storing.
        """
        layout_with_paths = self.__create_floor_layout()
        layout = layout_with_paths

        for row in layout[self.__inner: -self.__inner]:
            for cell, value in enumerate(row):
                if (
                    self.__inner <= cell < self.__y_axis - self.__inner
                    and value != self.__on_path
                ):
                    row[cell] = self.__taken
        return layout

    def __set_cells_for_waiting(self):
        """
        Sets cells for waiting in the ARFloorLayout.

        :return: The layout with cells set for waiting.
        """
        layout_with_storing = self.__set_cells_for_shelve_storing()
        layout = layout_with_storing

        for row in layout[self.__first_waiting_line : self.__outer]:
            # top horizontal
            for cell in range(len(row)):
                if (
                    self.__first_waiting_line
                    <= cell
                    < self.__x_axis - self.__first_waiting_line
                ):
                    row[cell] = self.__waiting

        for row in layout[self.__x_axis - self.__outer : -self.__first_waiting_line]:
            # bottom horizontal
            for cell in range(len(row)):
                if (
                    self.__first_waiting_line
                    <= cell
                    < self.__x_axis - self.__first_waiting_line
                ):
                    row[cell] = self.__waiting

        for row in layout[self.__first_waiting_line : -self.__first_waiting_line]:
            # vertical
            for cell in range(len(row)):
                if (
                    self.__first_waiting_line <= cell < self.__outer
                    and cell != self.__on_path
                    or self.__y_axis - self.__outer
                    <= cell
                    < self.__y_axis - self.__first_waiting_line
                    and cell != self.__on_path
                ):
                    row[cell] = self.__waiting

        return layout

    def __set_cells_for_picking_and_stowing(self):
        layout_with_waiting = self.__set_cells_for_waiting()
        layout = layout_with_waiting

        for cell in range(6, len(layout[0]) - 4, 8):
            # horizontal rows picking
            layout[0][cell] = self.__picking
            layout[-1][cell] = self.__picking
        for cell in range(10, len(layout[0]) - 4, 8):
            # horizontal rows stowing
            layout[0][cell] = self.__stowing
            layout[-1][cell] = self.__stowing

        for cell in range(4, len(layout) - 4, 8):
            # left and right columns picking
            layout[cell][0] = self.__picking
            layout[cell][-1] = self.__picking
        for cell in range(8, len(layout) - 4, 8):
            # left and right columns stowing
            layout[cell][0] = self.__stowing
            layout[cell][-1] = self.__stowing

        return layout

    def __set_cells_for_paths(self) -> List[List[NonNegativeInt]]:
        clean_floor = self.__set_cells_for_picking_and_stowing()
        layout = clean_floor
        for row in layout[self.__outer : -self.__outer]:
            # vertical left and right
            for cell in range(len(row)):
                if (
                    self.__outer <= cell < self.__inner
                    or self.__y_axis - self.__inner
                    <= cell
                    < self.__y_axis - self.__outer
                ):
                    row[cell] = self.__on_path
        for row in layout[self.__outer : self.__inner]:
            # horizontal top
            for cell in range(len(row)):
                if self.__inner <= cell <= self.__x_axis - self.__inner:
                    row[cell] = self.__on_path

        for row in layout[self.__x_axis - self.__inner : self.__x_axis - self.__outer]:
            # horizontal bottom
            for i in range(len(row)):
                if self.__inner <= i < self.__y_axis - self.__inner:
                    row[i] = self.__on_path

        for row in layout[
            self.__first_aisle : self.__x_axis - self.__inner : self.__aisle_gap
        ]:
            # aisles horizontal
            for cell in range(len(row)):
                row[cell] = self.__on_path
        for row in layout:
            # aisles vertical
            for cell in range(
                self.__first_aisle, self.__y_axis - self.__inner, self.__aisle_gap
            ):
                row[cell] = self.__on_path

        return layout

    def __set_charging_area(self):
        layout = self.__set_cells_for_paths()

        for row in layout[-self.__outer:]:
            for cell in range(len(row) - self.__outer, len(row)):
                row[cell] = self.__charging
        return layout

    def generate(self):
        return self.__floor_layout

    def __repr__(self):
        return "\n".join(
            " ".join(str(cell) for cell in row) for row in self.__floor_layout
        )
