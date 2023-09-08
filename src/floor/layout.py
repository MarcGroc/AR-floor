from pydantic import PositiveInt
from typing import List

from src.config.states import FloorLocationStates
from src.config.areas import FloorAreas
from src.floor.location import Location


class ARFloorLayout:
    """Creates floor layout and assign integer  to each field, there are states for floor location:"""

    def __init__(self):
        self.__x_axis: PositiveInt = 30
        self.__y_axis: PositiveInt = 30
        self._floor_layout = self.__set_charging_area()

    def __create_floor_layout(self) -> List[List[Location]]:
        return [
            [Location(row, col) for col in range(self.__x_axis)]
            for row in range(self.__y_axis)
        ]

    def __set_cells_for_shelve_storing(self) -> List[List[Location]]:
        """
        Sets the cells for shelve storing on the floor layout.

        :return: The updated floor layout with cells set for shelve storing.
        """
        layout_with_paths = self.__create_floor_layout()
        layout = layout_with_paths

        for row in layout[FloorAreas.INNER_FLOOR.value : -FloorAreas.INNER_FLOOR.value]:
            for cell, value in enumerate(row):
                if (
                    FloorAreas.INNER_FLOOR.value
                    <= cell
                    < self.__y_axis - FloorAreas.INNER_FLOOR.value
                ):
                    value.purpose = FloorLocationStates.STORING
        return layout

    def __set_cells_for_waiting(self) -> List[List[Location]]:
        """
        Sets cells for waiting in the ARFloorLayout.

        :return: The layout with cells set for waiting.
        """
        layout_with_storing = self.__set_cells_for_shelve_storing()
        layout = layout_with_storing

        for row in layout[
            FloorAreas.FIRST_WAITING_LINE.value : FloorAreas.OUTER_FLOOR.value
        ]:
            # top horizontal
            for cell in range(len(row)):
                if (
                    FloorAreas.FIRST_WAITING_LINE.value
                    <= cell
                    < self.__x_axis - FloorAreas.FIRST_WAITING_LINE.value
                ):
                    row[cell].purpose = FloorLocationStates.ON_PATH

        for row in layout[
            self.__x_axis
            - FloorAreas.OUTER_FLOOR.value : -FloorAreas.FIRST_WAITING_LINE.value
        ]:
            # bottom horizontal
            for cell in range(len(row)):
                if (
                    FloorAreas.FIRST_WAITING_LINE.value
                    <= cell
                    < self.__x_axis - FloorAreas.FIRST_WAITING_LINE.value
                ):
                    row[cell].purpose = FloorLocationStates.ON_PATH

        for row in layout[
            FloorAreas.FIRST_WAITING_LINE.value : -FloorAreas.FIRST_WAITING_LINE.value
        ]:
            # vertical
            for cell in range(len(row)):
                if (
                    FloorAreas.FIRST_WAITING_LINE.value
                    <= cell
                    < FloorAreas.OUTER_FLOOR.value
                    and cell != FloorLocationStates.ON_PATH
                    or self.__y_axis - FloorAreas.OUTER_FLOOR.value
                    <= cell
                    < self.__y_axis - FloorAreas.FIRST_WAITING_LINE.value
                    and cell != FloorLocationStates.ON_PATH
                ):
                    row[cell].purpose = FloorLocationStates.ON_PATH

        return layout

    def __set_cells_for_picking_and_stowing(self) -> List[List[Location]]:
        layout_with_waiting = self.__set_cells_for_waiting()
        layout = layout_with_waiting

        for cell in range(6, len(layout[0]) - 4, 8):
            # horizontal rows picking
            layout[0][cell].purpose = FloorLocationStates.PICKING
            layout[-1][cell].purpose = FloorLocationStates.PICKING
        for cell in range(10, len(layout[0]) - 4, 8):
            # horizontal rows stowing
            layout[0][cell].purpose = FloorLocationStates.STOWING
            layout[-1][cell].purpose = FloorLocationStates.STOWING

        for cell in range(4, len(layout) - 4, 8):
            # left and right columns picking
            layout[cell][0].purpose = FloorLocationStates.PICKING
            layout[cell][-1].purpose = FloorLocationStates.PICKING
        for cell in range(8, len(layout) - 4, 8):
            # left and right columns stowing
            layout[cell][0].purpose = FloorLocationStates.STOWING
            layout[cell][-1].purpose = FloorLocationStates.STOWING

        return layout

    def __set_cells_for_paths(self) -> List[List[Location]]:
        clean_floor = self.__set_cells_for_picking_and_stowing()
        layout = clean_floor
        for row in layout:
            for cell in range(len(row)):
                if row[cell].purpose is None:
                    row[cell].purpose = FloorLocationStates.WAITING

        for row in layout[FloorAreas.OUTER_FLOOR.value : -FloorAreas.OUTER_FLOOR.value]:
            # vertical left and right
            for cell in range(len(row)):
                if (
                    FloorAreas.OUTER_FLOOR.value <= cell < FloorAreas.INNER_FLOOR.value
                    or self.__y_axis - FloorAreas.INNER_FLOOR.value
                    <= cell
                    < self.__y_axis - FloorAreas.OUTER_FLOOR.value
                ):
                    row[cell].purpose = FloorLocationStates.ON_PATH
        for row in layout[FloorAreas.OUTER_FLOOR.value : FloorAreas.INNER_FLOOR.value]:
            # horizontal top
            for cell in range(len(row)):
                if (
                    FloorAreas.INNER_FLOOR.value
                    <= cell
                    <= self.__x_axis - FloorAreas.INNER_FLOOR.value
                ):
                    row[cell].purpose = FloorLocationStates.ON_PATH

        for row in layout[
            self.__x_axis
            - FloorAreas.INNER_FLOOR.value : self.__x_axis
            - FloorAreas.OUTER_FLOOR.value
        ]:
            # horizontal bottom
            for cell in range(len(row)):
                if (
                    FloorAreas.INNER_FLOOR.value
                    <= cell
                    < self.__y_axis - FloorAreas.INNER_FLOOR.value
                ):
                    row[cell].purpose = FloorLocationStates.ON_PATH

        for row in layout[
            FloorAreas.FIRST_AISLE.value : self.__x_axis
            - FloorAreas.INNER_FLOOR.value : FloorAreas.AISLE_GAP.value
        ]:
            # aisles horizontal
            for cell in range(len(row)):
                row[cell].purpose = FloorLocationStates.ON_PATH
        for row in layout:
            # aisles vertical
            for cell in range(
                FloorAreas.FIRST_AISLE.value,
                self.__y_axis - FloorAreas.INNER_FLOOR.value,
                FloorAreas.AISLE_GAP.value,
            ):
                row[cell].purpose = FloorLocationStates.ON_PATH

        return layout

    def __set_charging_area(self) -> List[List[Location]]:
        layout = self.__set_cells_for_paths()
        # todo move charging station to middle of grid

        for row in layout[-FloorAreas.OUTER_FLOOR.value :]:
            for cell in range(len(row) - FloorAreas.OUTER_FLOOR.value, len(row)):
                row[cell].purpose = FloorLocationStates.CHARGING
        return layout


    @property
    def generate(self) -> List[List[Location]]:
        return self._floor_layout

    def __str__(self):
        return "\n".join(
            " ".join(str(cell) for cell in row) for row in self._floor_layout
        )
