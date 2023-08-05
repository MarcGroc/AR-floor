from pydantic import PositiveInt, NonNegativeInt
from typing import List

# config/states.py
# enum - library - not needed
#
# class FloorLocationStates
#   """
#   NOT_TAKEN - represents ...
#   TAKEN -
#   ON_PATH
#   """
#
# class FloorAreas

# class FloorLocationStates:
#     """
#     Attributes:
#         NOT_TAKEN - it represents ...
#         ...
#     """
#     NOT_TAKEN = 0
#     TAKEN = 1
#     ON_PATH =  " "
#     WAITING = 3
#     PICKING = 4
#     STOWING = 5
#
# # other_file
# from config.states import FloorLocationStates
#
# if FloorLocationStates.NOT_TAKEN == ...:
#     pass

# text_str = "Marek"
# value_int = 30

# Possible states for floor locations
NOT_TAKEN = 0
TAKEN = 1
ON_PATH =  " "
WAITING = 3
PICKING = 4
STOWING = 5

# Floor areas
INNER_FLOOR = 6
OUTER_FLOOR = 3
AISLE_GAP = 4
FIRST_AISLE = 9
FIRST_WAITING_LINE = 1

class ARFloorLayout:
    """Creates floor layout and assign integer  to each field, there are states for floor location:
    Location taken and not taken are inner locations only for storing shelves, cannot be used as a part of path
    0 - 'not taken',location  available for robot to place shelf in that location if shelf won't be in use
    1 - 'taken',location  not available for robot to place shelf
    2 - 'on path' is external location used only for transit shelves, cannot be used for storing shelves
    3 - 'waiting' for interaction are only first three and last three fields where robot waiting for 'picking'
    or 'stowing' to be released
    4 - 'picking' location is available only on the edge fields of the floor,
     where human workers are able to pick items from robot
    5 - 'stowing' location is available only on the edge fields of the floor,
     where human workers are able to insert items to robot
    """

    def __init__(self):
        self.__x_axis: PositiveInt = 30
        self.__y_axis: PositiveInt = 30
        self.floor_layout = self.__assign_cells_for_waiting()

    def __create_floor_layout(self) -> List[List[NonNegativeInt]]:
        return [[NOT_TAKEN for _ in range(self.__x_axis)] for _ in range(self.__y_axis)]

    def __assign_cells_for_paths(self) -> List[List[NonNegativeInt]]:
        clean_floor = self.__create_floor_layout()
        layout = clean_floor

        for row in layout[OUTER_FLOOR:-OUTER_FLOOR]:
            # vertical left and right
            for i in range(len(row)):
                if (OUTER_FLOOR - 1) < i < INNER_FLOOR or self.__y_axis - (
                    INNER_FLOOR + 1
                ) < i < self.__y_axis - OUTER_FLOOR:
                    row[i] = ON_PATH

        for row in layout[OUTER_FLOOR:INNER_FLOOR]:
            # horizontal top
            for i in range(len(row)):
                if INNER_FLOOR <= i < self.__x_axis - INNER_FLOOR:
                    row[i] = ON_PATH

        for row in layout[self.__x_axis - INNER_FLOOR : self.__x_axis - OUTER_FLOOR]:
            # horizontal bottom
            for i in range(len(row)):
                if INNER_FLOOR <= i < self.__y_axis - INNER_FLOOR:
                    row[i] = ON_PATH

        for row in layout[FIRST_AISLE : self.__x_axis - INNER_FLOOR : AISLE_GAP]:
            # aisles horizontal
            for i in range(len(row)): # len(row) ---> size of row; range(X) ---> 0...X-1;
                if INNER_FLOOR <= i < self.__x_axis - INNER_FLOOR:
                    row[i] = ON_PATH

        for row in layout[INNER_FLOOR : self.__y_axis - INNER_FLOOR]:
            for i in range(FIRST_AISLE, self.__y_axis - INNER_FLOOR, AISLE_GAP):
                row[i] = ON_PATH
        return layout

    def __assign_cells_for_shelf_storing(self):
        layout_with_paths = self.__assign_cells_for_paths()
        layout = layout_with_paths

        for row in layout[INNER_FLOOR:-INNER_FLOOR]:
            for i, v in enumerate(row):
                if (INNER_FLOOR - 1) < i < self.__y_axis - INNER_FLOOR and v != ON_PATH:
                    row[i] = TAKEN
        return layout

    def __assign_cells_for_waiting(self):
        layout_with_storing = self.__assign_cells_for_shelf_storing()
        layout = layout_with_storing

        for row in layout[FIRST_WAITING_LINE: OUTER_FLOOR]:
            # top horizontal
            for i, v in enumerate(row):
                if FIRST_WAITING_LINE <= i < self.__x_axis - FIRST_WAITING_LINE:
                    row[i] = WAITING
        for row in layout[self.__x_axis - OUTER_FLOOR: -FIRST_WAITING_LINE]:
            # bottom horizontal
            for i, v in enumerate(row):
                if FIRST_WAITING_LINE <= i < self.__x_axis - FIRST_WAITING_LINE:
                    row[i] = WAITING

        for row in layout[FIRST_WAITING_LINE:-FIRST_WAITING_LINE]:
            # vertical
            for i, v in enumerate(row):
                if (FIRST_WAITING_LINE <= i < OUTER_FLOOR or
                        self.__y_axis - OUTER_FLOOR <= i < self.__y_axis - FIRST_WAITING_LINE):
                    row[i] = WAITING

        return layout

    def __repr__(self):
        return "\n".join(
            " ".join(str(cell) for cell in row) for row in self.floor_layout
        )


a = ARFloorLayout()
print(a)
