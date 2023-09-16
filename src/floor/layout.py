from pydantic import PositiveInt
from typing import List

from src.config.directions import Directions
from src.config.states import LocationStates
from src.config.areas import FloorAreas
from src.floor.location import Location

FLOOR_DIMENSION = 30


class FloorLayout:
    """Creates floor layout and assign Location to each field"""

    def __init__(self) -> None:
        self.__x_axis: PositiveInt = FLOOR_DIMENSION
        self.__y_axis: PositiveInt = FLOOR_DIMENSION
        # self._floor_layout = self.__set_charging_area()
        self.floor_layout = [
            [Location(row, col) for col in range(self.__x_axis)]
            for row in range(self.__y_axis)
        ]
        self.__set_layout_config()

    def __set_layout_config(self) -> None:
        self.__set_cells_for_paths()
        self.__set_cells_for_waiting()
        self.__set_cells_for_shelve_storing()
        self.__set_charging_area()
        self.__set_cells_for_picking_and_stowing()

    def __set_cells_purpose(self, row_start, row_end, col_start, col_end, purpose, filter_purpose=None, heading=None) -> None:
        for row in self.floor_layout[row_start:row_end]:
            for cell in row[col_start:col_end]:
                if filter_purpose is None or cell.purpose == filter_purpose:
                    cell.purpose = purpose
                    if heading:
                        cell.heading = heading

    def __set_cells_for_shelve_storing(self) -> None:
        self.__set_cells_purpose(
            FloorAreas.INNER_FLOOR.value,
            -FloorAreas.INNER_FLOOR.value,
            FloorAreas.INNER_FLOOR.value,
            self.__y_axis - FloorAreas.INNER_FLOOR.value,
            LocationStates.STORING,
        )

    def __set_cells_for_waiting(self) -> None:
        # Top horizontal
        self.__set_cells_purpose(
            FloorAreas.FIRST_WAITING_LINE.value,
            FloorAreas.OUTER_FLOOR.value,
            FloorAreas.FIRST_WAITING_LINE.value,
            self.__x_axis - FloorAreas.FIRST_WAITING_LINE.value,
            LocationStates.WAITING,
        )

        # Bottom horizontal
        self.__set_cells_purpose(
            self.__x_axis - FloorAreas.OUTER_FLOOR.value,
            -FloorAreas.FIRST_WAITING_LINE.value,
            FloorAreas.FIRST_WAITING_LINE.value,
            self.__x_axis - FloorAreas.FIRST_WAITING_LINE.value,
            LocationStates.WAITING,
        )

        # Vertical - Left
        self.__set_cells_purpose(
            FloorAreas.FIRST_WAITING_LINE.value,
            -FloorAreas.FIRST_WAITING_LINE.value,
            FloorAreas.FIRST_WAITING_LINE.value,
            FloorAreas.OUTER_FLOOR.value,
            LocationStates.WAITING,
        )

        # Vertical - Right
        self.__set_cells_purpose(
            FloorAreas.FIRST_WAITING_LINE.value,
            -FloorAreas.FIRST_WAITING_LINE.value,
            self.__y_axis - FloorAreas.OUTER_FLOOR.value,
            self.__y_axis - FloorAreas.FIRST_WAITING_LINE.value,
            LocationStates.WAITING,
        )

    def __set_cells_for_picking_and_stowing(self) -> None:
        for cell in range(6, self.__x_axis - 4, 8):
            self.__set_cells_purpose(0, 1, cell, cell + 1, LocationStates.PICKING, Directions.NORTH)
            self.__set_cells_purpose(-1, None, cell, cell + 1, LocationStates.PICKING, Directions.SOUTH)

        for cell in range(10, self.__x_axis - 4, 8):
            self.__set_cells_purpose(0, 1, cell, cell + 1, LocationStates.STOWING, Directions.NORTH)
            self.__set_cells_purpose(-1, None, cell, cell + 1, LocationStates.STOWING, Directions.SOUTH)

        for cell in range(4, self.__y_axis - 4, 8):
            self.__set_cells_purpose(cell, cell + 1, 0, 1, LocationStates.PICKING, Directions.WEST)
            self.__set_cells_purpose(cell, cell + 1, -1, None, LocationStates.PICKING, Directions.EAST)

        for cell in range(8, self.__y_axis - 4, 8):
            self.__set_cells_purpose(cell, cell + 1, 0, 1, LocationStates.STOWING, Directions.WEST)
            self.__set_cells_purpose(cell, cell + 1, -1, None, LocationStates.STOWING, Directions.EAST)

    def __set_cells_for_paths(self) -> None:
        # Defaulting all None purpose cells to NOT_TAKEN
        self.__set_cells_purpose(
            0,
            self.__x_axis,
            0,
            self.__y_axis,
            LocationStates.NOT_TAKEN,
            filter_purpose=None,
        )

        # Vertical left and right
        self.__set_cells_purpose(
            FloorAreas.OUTER_FLOOR.value,
            -FloorAreas.OUTER_FLOOR.value,
            FloorAreas.OUTER_FLOOR.value,
            FloorAreas.INNER_FLOOR.value,
            LocationStates.ON_PATH,
        )
        self.__set_cells_purpose(
            FloorAreas.OUTER_FLOOR.value,
            -FloorAreas.OUTER_FLOOR.value,
            self.__y_axis - FloorAreas.INNER_FLOOR.value,
            self.__y_axis - FloorAreas.OUTER_FLOOR.value,
            LocationStates.ON_PATH,
        )

        # Horizontal top
        self.__set_cells_purpose(
            FloorAreas.OUTER_FLOOR.value,
            FloorAreas.INNER_FLOOR.value,
            FloorAreas.INNER_FLOOR.value,
            self.__x_axis - FloorAreas.INNER_FLOOR.value,
            LocationStates.ON_PATH,
        )

        # Horizontal bottom
        self.__set_cells_purpose(
            self.__x_axis - FloorAreas.INNER_FLOOR.value,
            self.__x_axis - FloorAreas.OUTER_FLOOR.value,
            FloorAreas.INNER_FLOOR.value,
            self.__y_axis - FloorAreas.INNER_FLOOR.value,
            LocationStates.ON_PATH,
        )

        # Aisles horizontal
        for row_start in range(
            FloorAreas.FIRST_AISLE.value,
            self.__x_axis - FloorAreas.INNER_FLOOR.value,
            FloorAreas.AISLE_GAP.value,
        ):
            self.__set_cells_purpose(
                row_start, row_start + 1, 0, self.__y_axis, LocationStates.ON_PATH
            )

        # Aisles vertical
        for col_start in range(
            FloorAreas.FIRST_AISLE.value,
            self.__y_axis - FloorAreas.INNER_FLOOR.value,
            FloorAreas.AISLE_GAP.value,
        ):
            self.__set_cells_purpose(
                0, self.__x_axis, col_start, col_start + 1, LocationStates.ON_PATH
            )

    def __set_charging_area(self) -> None:
        mid_cell = len(self.floor_layout) // 2
        charging_area_size = 3
        self.__set_cells_purpose(
            mid_cell - charging_area_size,
            mid_cell + charging_area_size,
            mid_cell - charging_area_size,
            mid_cell + charging_area_size,
            LocationStates.CHARGING,
        )

    def __str__(self):
        return "\n".join(
            " ".join(str(cell) for cell in row) for row in self.floor_layout
        )
        # def __create_floor_layout(self) -> List[List[Location]]:

    #     """Sets Location on each field"""
    #     return [
    #         [Location(row, col) for col in range(self.__x_axis)]
    #         for row in range(self.__y_axis)
    #     ]

    # def __set_cells_for_shelve_storing(self) -> List[List[Location]]:
    #     """
    #     Sets the cells for shelve storing on the floor layout.
    #
    #     :return: The updated floor layout with cells set for shelve storing.
    #     """
    #     layout_with_paths = self.__create_floor_layout()
    #     layout = layout_with_paths
    #
    #     for row in layout[FloorAreas.INNER_FLOOR.value : -FloorAreas.INNER_FLOOR.value]:
    #         for cell, value in enumerate(row):
    #             if (
    #                 FloorAreas.INNER_FLOOR.value
    #                 <= cell
    #                 < self.__y_axis - FloorAreas.INNER_FLOOR.value
    #             ):
    #                 value.purpose = LocationStates.STORING
    #     return layout
    #
    # def __set_cells_for_waiting(self) -> List[List[Location]]:
    #     """
    #     Sets cells where robot is waiting for interaction with workstation.
    #
    #     :return: The layout with cells set for waiting.
    #     """
    #     layout_with_storing = self.__set_cells_for_shelve_storing()
    #     layout = layout_with_storing
    #
    #     for row in layout[
    #         FloorAreas.FIRST_WAITING_LINE.value : FloorAreas.OUTER_FLOOR.value
    #     ]:
    #         # top horizontal
    #         for cell in range(len(row)):
    #             if (
    #                 FloorAreas.FIRST_WAITING_LINE.value
    #                 <= cell
    #                 < self.__x_axis - FloorAreas.FIRST_WAITING_LINE.value
    #             ):
    #                 row[cell].purpose = LocationStates.ON_PATH
    #
    #     for row in layout[
    #         self.__x_axis
    #         - FloorAreas.OUTER_FLOOR.value : -FloorAreas.FIRST_WAITING_LINE.value
    #     ]:
    #         # bottom horizontal
    #         for cell in range(len(row)):
    #             if (
    #                 FloorAreas.FIRST_WAITING_LINE.value
    #                 <= cell
    #                 < self.__x_axis - FloorAreas.FIRST_WAITING_LINE.value
    #             ):
    #                 row[cell].purpose = LocationStates.ON_PATH
    #
    #     for row in layout[
    #         FloorAreas.FIRST_WAITING_LINE.value : -FloorAreas.FIRST_WAITING_LINE.value
    #     ]:
    #         # vertical
    #         for cell in range(len(row)):
    #             if (
    #                 FloorAreas.FIRST_WAITING_LINE.value
    #                 <= cell
    #                 < FloorAreas.OUTER_FLOOR.value
    #                 and cell != LocationStates.ON_PATH
    #                 or self.__y_axis - FloorAreas.OUTER_FLOOR.value
    #                 <= cell
    #                 < self.__y_axis - FloorAreas.FIRST_WAITING_LINE.value
    #                 and cell != LocationStates.ON_PATH
    #             ):
    #                 row[cell].purpose = LocationStates.ON_PATH
    #
    #     return layout
    #
    # def __set_cells_for_picking_and_stowing(self) -> List[List[Location]]:
    #     """Sets cells for workstations where items can be added or removed"""
    #     layout_with_waiting = self.__set_cells_for_waiting()
    #     layout = layout_with_waiting
    #
    #     for cell in range(6, len(layout[0]) - 4, 8):
    #         # horizontal rows picking
    #         layout[0][cell].purpose = LocationStates.PICKING
    #         layout[0][cell].heading = Directions.NORTH
    #         layout[-1][cell].purpose = LocationStates.PICKING
    #         layout[-1][cell].heading = Directions.SOUTH
    #     for cell in range(10, len(layout[0]) - 4, 8):
    #         # horizontal rows stowing
    #         layout[0][cell].purpose = LocationStates.STOWING
    #         layout[0][cell].heading = Directions.NORTH
    #         layout[-1][cell].purpose = LocationStates.STOWING
    #         layout[-1][cell].heading = Directions.SOUTH
    #
    #     for cell in range(4, len(layout) - 4, 8):
    #         # left and right columns picking
    #         layout[cell][0].purpose = LocationStates.PICKING
    #         layout[cell][0].heading = Directions.WEST
    #         layout[cell][-1].purpose = LocationStates.PICKING
    #         layout[cell][-1].heading = Directions.EAST
    #     for cell in range(8, len(layout) - 4, 8):
    #         # left and right columns stowing
    #         layout[cell][0].purpose = LocationStates.STOWING
    #         layout[cell][0].heading = Directions.WEST
    #         layout[cell][-1].purpose = LocationStates.STOWING
    #         layout[cell][-1].heading = Directions.EAST
    #
    #     return layout
    #
    # def __set_cells_for_paths(self) -> List[List[Location]]:
    #     """Set cells on which robot can transport shelve"""
    #     clean_floor = self.__set_cells_for_picking_and_stowing()
    #     layout = clean_floor
    #     for row in layout:
    #         for cell in range(len(row)):
    #             if row[cell].purpose is None:
    #                 row[cell].purpose = LocationStates.NOT_TAKEN
    #
    #     for row in layout[FloorAreas.OUTER_FLOOR.value : -FloorAreas.OUTER_FLOOR.value]:
    #         # vertical left and right
    #         for cell in range(len(row)):
    #             if (
    #                 FloorAreas.OUTER_FLOOR.value <= cell < FloorAreas.INNER_FLOOR.value
    #                 or self.__y_axis - FloorAreas.INNER_FLOOR.value
    #                 <= cell
    #                 < self.__y_axis - FloorAreas.OUTER_FLOOR.value
    #             ):
    #                 row[cell].purpose = LocationStates.ON_PATH
    #     for row in layout[FloorAreas.OUTER_FLOOR.value : FloorAreas.INNER_FLOOR.value]:
    #         # horizontal top
    #         for cell in range(len(row)):
    #             if (
    #                 FloorAreas.INNER_FLOOR.value
    #                 <= cell
    #                 <= self.__x_axis - FloorAreas.INNER_FLOOR.value
    #             ):
    #                 row[cell].purpose = LocationStates.ON_PATH
    #
    #     for row in layout[
    #         self.__x_axis
    #         - FloorAreas.INNER_FLOOR.value : self.__x_axis
    #         - FloorAreas.OUTER_FLOOR.value
    #     ]:
    #         # horizontal bottom
    #         for cell in range(len(row)):
    #             if (
    #                 FloorAreas.INNER_FLOOR.value
    #                 <= cell
    #                 < self.__y_axis - FloorAreas.INNER_FLOOR.value
    #             ):
    #                 row[cell].purpose = LocationStates.ON_PATH
    #
    #     for row in layout[
    #         FloorAreas.FIRST_AISLE.value : self.__x_axis
    #         - FloorAreas.INNER_FLOOR.value : FloorAreas.AISLE_GAP.value
    #     ]:
    #         # aisles horizontal
    #         for cell in range(len(row)):
    #             row[cell].purpose = LocationStates.ON_PATH
    #     for row in layout:
    #         # aisles vertical
    #         for cell in range(
    #             FloorAreas.FIRST_AISLE.value,
    #             self.__y_axis - FloorAreas.INNER_FLOOR.value,
    #             FloorAreas.AISLE_GAP.value,
    #         ):
    #             row[cell].purpose = LocationStates.ON_PATH
    #
    #     return layout
    #
    # def __set_charging_area(self) -> List[List[Location]]:
    #     """Set cells where robots can charge batteries"""
    #     layout = self.__set_cells_for_paths()
    #     mid_cell = len(layout) // 2
    #     charging_area_size = 3
    #     for row in range(mid_cell - charging_area_size, mid_cell + charging_area_size):
    #         for cell in range(
    #             mid_cell - charging_area_size, mid_cell + charging_area_size
    #         ):
    #             layout[row][cell].purpose = LocationStates.CHARGING
    #
    #     return layout

    # @property
    # def initialize(self) -> List[List[Location]]:
    #     return self._floor_layout

    # def __str__(self):
    #     return "\n".join(" ".join(str(cell) for cell in row) for row in self._floor_layout)
