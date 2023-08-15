from pydantic import PositiveInt, NonNegativeInt
from typing import List

from src.config.states import FloorLocationStates
from src.config.areas import FloorAreas


class ARFloorLayout:
    """Creates floor layout and assign integer  to each field, there are states for floor location:"""

    def __init__(self):
        self.__x_axis: PositiveInt = 30
        self.__y_axis: PositiveInt = 30
        self.floor_layout = self.__assign_cells_for_picking_and_stowing()

    def __create_floor_layout(self) -> List[List[NonNegativeInt]]:
        return [
            [FloorLocationStates.NOT_TAKEN.value for _ in range(self.__x_axis)]
            for _ in range(self.__y_axis)
        ]

    def __assign_cells_for_paths(self) -> List[List[NonNegativeInt]]:
        clean_floor = self.__create_floor_layout()
        layout = clean_floor
        # TODO dodać wyjazd z alejki
        for row in layout[FloorAreas.OUTER_FLOOR.value : -FloorAreas.OUTER_FLOOR.value]:
            # vertical left and right
            for i in range(len(row)):
                if (
                    FloorAreas.OUTER_FLOOR.value - 1
                ) < i < FloorAreas.INNER_FLOOR.value or self.__y_axis - (
                    FloorAreas.INNER_FLOOR.value + 1
                ) < i < self.__y_axis - FloorAreas.OUTER_FLOOR.value:
                    row[i] = FloorLocationStates.ON_PATH.value

        for row in layout[FloorAreas.OUTER_FLOOR.value : FloorAreas.INNER_FLOOR.value]:
            # horizontal top
            for i in range(len(row)):
                if (
                    FloorAreas.INNER_FLOOR.value
                    <= i
                    < self.__x_axis - FloorAreas.INNER_FLOOR.value
                ):
                    row[i] = FloorLocationStates.ON_PATH.value

        for row in layout[
            self.__x_axis
            - FloorAreas.INNER_FLOOR.value : self.__x_axis
            - FloorAreas.OUTER_FLOOR.value
        ]:
            # horizontal bottom
            for i in range(len(row)):
                if (
                    FloorAreas.INNER_FLOOR.value
                    <= i
                    < self.__y_axis - FloorAreas.INNER_FLOOR.value
                ):
                    row[i] = FloorLocationStates.ON_PATH.value

        for row in layout[
            FloorAreas.FIRST_AISLE.value : self.__x_axis
            - FloorAreas.INNER_FLOOR.value : FloorAreas.AISLE_GAP.value
        ]:
            # aisles horizontal
            for i in range(len(row)):
                if (
                    FloorAreas.INNER_FLOOR.value
                    <= i
                    < self.__x_axis - FloorAreas.INNER_FLOOR.value
                ):
                    row[i] = FloorLocationStates.ON_PATH.value

        for row in layout[
            FloorAreas.INNER_FLOOR.value : self.__y_axis - FloorAreas.INNER_FLOOR.value
        ]:
            for i in range(
                FloorAreas.FIRST_AISLE.value,
                self.__y_axis - FloorAreas.INNER_FLOOR.value,
                FloorAreas.AISLE_GAP.value,
            ):
                row[i] = FloorLocationStates.ON_PATH.value
        return layout

    def __assign_cells_for_shelf_storing(self):
        layout_with_paths = self.__assign_cells_for_paths()
        layout = layout_with_paths

        for row in layout[FloorAreas.INNER_FLOOR.value : -FloorAreas.INNER_FLOOR.value]:
            for i, v in enumerate(row):
                if (
                    (FloorAreas.INNER_FLOOR.value - 1)
                    < i
                    < self.__y_axis - FloorAreas.INNER_FLOOR.value
                    and v != FloorLocationStates.ON_PATH
                ):
                    row[i] = FloorLocationStates.TAKEN.value
        return layout

    def __assign_cells_for_waiting(self):
        layout_with_storing = self.__assign_cells_for_shelf_storing()
        layout = layout_with_storing

        for row in layout[
            FloorAreas.FIRST_WAITING_LINE.value : FloorAreas.OUTER_FLOOR.value
        ]:
            # top horizontal
            for i in range(len(row)):
                if (
                    FloorAreas.FIRST_WAITING_LINE.value
                    <= i
                    < self.__x_axis - FloorAreas.FIRST_WAITING_LINE.value
                ):
                    row[i] = FloorLocationStates.WAITING.value
        for row in layout[
            self.__x_axis
            - FloorAreas.OUTER_FLOOR.value : -FloorAreas.FIRST_WAITING_LINE.value
        ]:
            # bottom horizontal
            for i in range(len(row)):
                if (
                    FloorAreas.FIRST_WAITING_LINE.value
                    <= i
                    < self.__x_axis - FloorAreas.FIRST_WAITING_LINE.value
                ):
                    row[i] = FloorLocationStates.WAITING.value

        for row in layout[
            FloorAreas.FIRST_WAITING_LINE.value : -FloorAreas.FIRST_WAITING_LINE.value
        ]:
            # vertical
            for i in range(len(row)):
                if (
                    FloorAreas.FIRST_WAITING_LINE.value
                    <= i
                    < FloorAreas.OUTER_FLOOR.value
                    or self.__y_axis - FloorAreas.OUTER_FLOOR.value
                    <= i
                    < self.__y_axis - FloorAreas.FIRST_WAITING_LINE.value
                ):
                    row[i] = FloorLocationStates.WAITING.value

        return layout

    def __assign_cells_for_picking_and_stowing(self):
        layout_with_waiting = self.__assign_cells_for_waiting()
        layout = layout_with_waiting

        for i in range(2, len(layout[0]) - 2):
            # top row
            if i % 2 == 0:
                layout[0][i] = FloorLocationStates.PICKING.value
            else:
                layout[0][i] = FloorLocationStates.STOWING.value
        for i in range(2, len(layout[-1]) - 2):
            # bottom row
            if i % 2 == 0:
                layout[-1][i] = FloorLocationStates.PICKING.value
            else:
                layout[-1][i] = FloorLocationStates.STOWING.value

        for i in range(2, len(layout) - 2):
            # left and right columns
            if i % 2 == 0:
                layout[i][0] = FloorLocationStates.PICKING.value
                layout[i][-1] = FloorLocationStates.PICKING.value
            else:
                layout[i][0] = FloorLocationStates.STOWING.value
                layout[i][-1] = FloorLocationStates.STOWING.value
        return layout

    def __repr__(self):
        return "\n".join(
            " ".join(str(cell) for cell in row) for row in self.floor_layout
        )


a = ARFloorLayout()
print(a)
