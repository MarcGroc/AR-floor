from pydantic import PositiveInt, NonNegativeInt
from typing import List

from src.config.states import FloorLocationStates
from src.config.areas import FloorAreas
from src.floor.location import Location


class ARFloorLayout:
    """Creates floor layout and assign integer  to each field, there are states for floor location:"""

    def __init__(self):
        self.__x_axis: PositiveInt = 30
        self.__y_axis: PositiveInt = 30
        # for state in FloorLocationStates:
        #     setattr(self, f"{state.name.lower()}", state.value)
        #
        # for area in FloorAreas:
        #     setattr(self, f"_{area.name.lower()}", area.value)

        self._outer = FloorAreas.OUTER_FLOOR
        self._inner = FloorAreas.INNER_FLOOR
        self._first_aisle = FloorAreas.FIRST_AISLE
        self._aisle_gap = FloorAreas.AISLE_GAP
        self._waiting = FloorLocationStates.WAITING
        self._first_waiting_line = FloorAreas.FIRST_WAITING_LINE
        self._on_path = FloorLocationStates.ON_PATH
        self._not_taken = FloorLocationStates.NOT_TAKEN
        self._taken = FloorLocationStates.TAKEN
        self._picking = FloorLocationStates.PICKING
        self._stowing = FloorLocationStates.STOWING
        self._charging = FloorLocationStates.CHARGING
        self._storing = FloorLocationStates.STORING
        self._floor_layout = self.__set_charging_area()

    def __create_floor_layout(self) -> List[List[NonNegativeInt]]:
        return [[None for _ in range(self.__x_axis)] for _ in range(self.__y_axis)]

    def __set_cells_for_shelve_storing(self) -> List[List[Location]]:
        """
        Sets the cells for shelve storing on the floor layout.

        :return: The updated floor layout with cells set for shelve storing.
        """
        layout_with_paths = self.__create_floor_layout()
        layout = layout_with_paths

        for row in layout[self._inner.value : -self._inner.value]:
            for cell, value in enumerate(row):
                if (
                    self._inner.value <= cell < self.__y_axis - self._inner.value
                    and value != self._on_path
                ):
                    row[cell] = Location(self._storing, None)
        return layout

    def __set_cells_for_waiting(self) -> List[List[Location]]:
        """
        Sets cells for waiting in the ARFloorLayout.

        :return: The layout with cells set for waiting.
        """
        layout_with_storing = self.__set_cells_for_shelve_storing()
        layout = layout_with_storing

        for row in layout[self._first_waiting_line.value : self._outer.value]:
            # top horizontal
            for cell in range(len(row)):
                if (
                    self._first_waiting_line.value
                    <= cell
                    < self.__x_axis - self._first_waiting_line.value
                ):
                    row[cell] = Location(self._waiting, None)

        for row in layout[
            self.__x_axis - self._outer.value : -self._first_waiting_line.value
        ]:
            # bottom horizontal
            for cell in range(len(row)):
                if (
                    self._first_waiting_line.value
                    <= cell
                    < self.__x_axis - self._first_waiting_line.value
                ):
                    row[cell] = Location(self._waiting, None)

        for row in layout[
            self._first_waiting_line.value : -self._first_waiting_line.value
        ]:
            # vertical
            for cell in range(len(row)):
                if (
                    self._first_waiting_line.value <= cell < self._outer.value
                    and cell != self._on_path
                    or self.__y_axis - self._outer.value
                    <= cell
                    < self.__y_axis - self._first_waiting_line.value
                    and cell != self._on_path
                ):
                    row[cell] = Location(self._waiting, None)

        return layout

    def __set_cells_for_picking_and_stowing(self) -> List[List[Location]]:
        layout_with_waiting = self.__set_cells_for_waiting()
        layout = layout_with_waiting

        for cell in range(6, len(layout[0]) - 4, 8):
            # horizontal rows picking
            layout[0][cell] = Location(self._picking, None)
            layout[-1][cell] = Location(self._picking, None)
        for cell in range(10, len(layout[0]) - 4, 8):
            # horizontal rows stowing
            layout[0][cell] = Location(self._stowing, None)
            layout[-1][cell] = Location(self._stowing, None)

        for cell in range(4, len(layout) - 4, 8):
            # left and right columns picking
            layout[cell][0] = Location(self._picking, None)
            layout[cell][-1] = Location(self._picking, None)
        for cell in range(8, len(layout) - 4, 8):
            # left and right columns stowing
            layout[cell][0] = Location(self._stowing, None)
            layout[cell][-1] = Location(self._stowing, None)

        return layout

    def __set_cells_for_paths(self) -> List[List[Location]]:
        clean_floor = self.__set_cells_for_picking_and_stowing()
        layout = clean_floor
        for row in layout[self._outer.value : -self._outer.value]:
            # vertical left and right
            for cell in range(len(row)):
                if (
                    self._outer.value <= cell < self._inner.value
                    or self.__y_axis - self._inner.value
                    <= cell
                    < self.__y_axis - self._outer.value
                ):
                    row[cell] = Location(self._on_path, None)
        for row in layout[self._outer.value : self._inner.value]:
            # horizontal top
            for cell in range(len(row)):
                if self._inner.value <= cell <= self.__x_axis - self._inner.value:
                    row[cell] = Location(self._on_path, None)

        for row in layout[
            self.__x_axis - self._inner.value : self.__x_axis - self._outer.value
        ]:
            # horizontal bottom
            for cell in range(len(row)):
                if self._inner.value <= cell < self.__y_axis - self._inner.value:
                    row[cell] = Location(self._on_path, None)

        for row in layout[
            self._first_aisle.value : self.__x_axis
            - self._inner.value : self._aisle_gap.value
        ]:
            # aisles horizontal
            for cell in range(len(row)):
                row[cell] = Location(self._on_path, None)
        for row in layout:
            # aisles vertical
            for cell in range(
                self._first_aisle.value,
                self.__y_axis - self._inner.value,
                self._aisle_gap.value,
            ):
                row[cell] = Location(self._on_path, None)

        return layout

    def __set_charging_area(self)-> List[List[Location]]:
        layout = self.__set_cells_for_paths()

        for row in layout[-self._outer.value :]:
            for cell in range(len(row) - self._outer.value, len(row)):
                row[cell] = Location(self._charging, None)
        return layout

    @property
    def generate(self) -> List[List[NonNegativeInt]]:
        return self._floor_layout

    def __repr__(self):
        return "\n".join(
            " ".join(str(cell) for cell in row) for row in self._floor_layout
        )
