from typing import Optional

from pydantic import PositiveInt

from src.config.directions import Directions
from src.config.states import LocationStates
from src.config.areas import FloorAreas
from src.floor.location import Location

WORKSTATION_GAP = 8
CORNER_WORKSTATION = 4
FIRST_PICKING_WORKSTATION = 6
FIRST_STOWING_WORKSTATION = 10

CHARGING_AREA_SIZE = 3

class FloorLayout:
    """Creates floor layout and assign Location to each field"""

    def __init__(self, dimension: PositiveInt) -> None:
        self._x_axis = dimension
        self._y_axis = dimension
        self.floor_layout = self._initialize()
        self._set_layout_config()

    def _initialize(self) -> list[list[Location]]:
        return [
            [Location(row, col) for col in range(self._x_axis)]
            for row in range(self._y_axis)
        ]

    def _set_layout_config(self) -> None:
        self._initialize_paths()
        self._initialize_paths()
        self._initialize_shelve_storing_areas()
        self._initialize_charging_area()
        self._initialize_picking_and_stowing_areas()

    def _assign_purpose_to_cells(
        self,
        row_start: int,
        row_end: int,
        col_start: int,
        col_end: int,
        purpose: LocationStates,
        filter_purpose: Optional[LocationStates] = None,
        heading: Optional[Directions] = None,
    ) -> None:
        for row in self.floor_layout[row_start:row_end]:
            for cell in row[col_start:col_end]:
                if filter_purpose is None or cell.purpose == filter_purpose:
                    cell.purpose = purpose
                    if heading:
                        cell.heading = heading

    def _initialize_shelve_storing_areas(self) -> None:
        self._assign_purpose_to_cells(
            FloorAreas.INNER_FLOOR.value,
            -FloorAreas.INNER_FLOOR.value,
            FloorAreas.INNER_FLOOR.value,
            self._y_axis - FloorAreas.INNER_FLOOR.value,
            LocationStates.STORING,
        )

    def _initialize_waiting_areas(self) -> None:
        # Top horizontal
        self._assign_purpose_to_cells(
            FloorAreas.FIRST_WAITING_LINE.value,
            FloorAreas.OUTER_FLOOR.value,
            FloorAreas.FIRST_WAITING_LINE.value,
            self._x_axis - FloorAreas.FIRST_WAITING_LINE.value,
            LocationStates.WAITING,
        )

        # Bottom horizontal
        self._assign_purpose_to_cells(
            self._x_axis - FloorAreas.OUTER_FLOOR.value,
            -FloorAreas.FIRST_WAITING_LINE.value,
            FloorAreas.FIRST_WAITING_LINE.value,
            self._x_axis - FloorAreas.FIRST_WAITING_LINE.value,
            LocationStates.WAITING,
        )

        # Vertical - Left
        self._assign_purpose_to_cells(
            FloorAreas.FIRST_WAITING_LINE.value,
            -FloorAreas.FIRST_WAITING_LINE.value,
            FloorAreas.FIRST_WAITING_LINE.value,
            FloorAreas.OUTER_FLOOR.value,
            LocationStates.WAITING,
        )

        # Vertical - Right
        self._assign_purpose_to_cells(
            FloorAreas.FIRST_WAITING_LINE.value,
            -FloorAreas.FIRST_WAITING_LINE.value,
            self._y_axis - FloorAreas.OUTER_FLOOR.value,
            self._y_axis - FloorAreas.FIRST_WAITING_LINE.value,
            LocationStates.WAITING,
        )

    def _initialize_picking_and_stowing_areas(self) -> None:
        filter_purpose = (
            LocationStates.NOT_TAKEN
        )  # Cells to be overwritten must be NOT_TAKEN

        for cell in range(
            FIRST_PICKING_WORKSTATION,
            self._x_axis - CORNER_WORKSTATION,
            WORKSTATION_GAP,
        ):
            self._assign_purpose_to_cells(
                0,
                1,
                cell,
                cell + 1,
                LocationStates.PICKING,
                filter_purpose,
                Directions.NORTH,
            )
            self._assign_purpose_to_cells(
                -1,
                None,
                cell,
                cell + 1,
                LocationStates.PICKING,
                filter_purpose,
                Directions.SOUTH,
            )

        for cell in range(
            FIRST_STOWING_WORKSTATION,
            self._x_axis - CORNER_WORKSTATION,
            WORKSTATION_GAP,
        ):
            self._assign_purpose_to_cells(
                0,
                1,
                cell,
                cell + 1,
                LocationStates.STOWING,
                filter_purpose,
                Directions.NORTH,
            )
            self._assign_purpose_to_cells(
                -1,
                None,
                cell,
                cell + 1,
                LocationStates.STOWING,
                filter_purpose,
                Directions.SOUTH,
            )

        for cell in range(
            CORNER_WORKSTATION, self._y_axis - CORNER_WORKSTATION, WORKSTATION_GAP
        ):
            self._assign_purpose_to_cells(
                cell,
                cell + 1,
                0,
                1,
                LocationStates.PICKING,
                filter_purpose,
                Directions.WEST,
            )
            self._assign_purpose_to_cells(
                cell,
                cell + 1,
                -1,
                None,
                LocationStates.PICKING,
                filter_purpose,
                Directions.EAST,
            )

        for cell in range(
            WORKSTATION_GAP, self._y_axis - CORNER_WORKSTATION, WORKSTATION_GAP
        ):
            self._assign_purpose_to_cells(
                cell,
                cell + 1,
                0,
                1,
                LocationStates.STOWING,
                filter_purpose,
                Directions.WEST,
            )
            self._assign_purpose_to_cells(
                cell,
                cell + 1,
                -1,
                None,
                LocationStates.STOWING,
                filter_purpose,
                Directions.EAST,
            )

    def _initialize_paths(self) -> None:
        # Defaulting all None purpose cells to NOT_TAKEN
        self._assign_purpose_to_cells(
            0,
            self._x_axis,
            0,
            self._y_axis,
            LocationStates.NOT_TAKEN,
            filter_purpose=None,
        )

        # Vertical left and right
        self._assign_purpose_to_cells(
            FloorAreas.OUTER_FLOOR.value,
            -FloorAreas.OUTER_FLOOR.value,
            FloorAreas.OUTER_FLOOR.value,
            FloorAreas.INNER_FLOOR.value,
            LocationStates.ON_PATH,
        )
        self._assign_purpose_to_cells(
            FloorAreas.OUTER_FLOOR.value,
            -FloorAreas.OUTER_FLOOR.value,
            self._y_axis - FloorAreas.INNER_FLOOR.value,
            self._y_axis - FloorAreas.OUTER_FLOOR.value,
            LocationStates.ON_PATH,
        )

        # Horizontal top
        self._assign_purpose_to_cells(
            FloorAreas.OUTER_FLOOR.value,
            FloorAreas.INNER_FLOOR.value,
            FloorAreas.INNER_FLOOR.value,
            self._x_axis - FloorAreas.INNER_FLOOR.value,
            LocationStates.ON_PATH,
        )

        # Horizontal bottom
        self._assign_purpose_to_cells(
            self._x_axis - FloorAreas.INNER_FLOOR.value,
            self._x_axis - FloorAreas.OUTER_FLOOR.value,
            FloorAreas.INNER_FLOOR.value,
            self._y_axis - FloorAreas.INNER_FLOOR.value,
            LocationStates.ON_PATH,
        )

        # Aisles horizontal
        for row_start in range(
            FloorAreas.FIRST_AISLE.value,
            self._x_axis - FloorAreas.INNER_FLOOR.value,
            FloorAreas.AISLE_GAP.value,
        ):
            self._assign_purpose_to_cells(
                row_start, row_start + 1, 0, self._y_axis, LocationStates.ON_PATH
            )

        # Aisles vertical
        for col_start in range(
            FloorAreas.FIRST_AISLE.value,
            self._y_axis - FloorAreas.INNER_FLOOR.value,
            FloorAreas.AISLE_GAP.value,
        ):
            self._assign_purpose_to_cells(
                0, self._x_axis, col_start, col_start + 1, LocationStates.ON_PATH
            )

    def _initialize_charging_area(self) -> None:
        mid_cell = round(len(self.floor_layout) / 2)
        self._assign_purpose_to_cells(
            mid_cell - CHARGING_AREA_SIZE,
            mid_cell + CHARGING_AREA_SIZE,
            mid_cell - CHARGING_AREA_SIZE,
            mid_cell + CHARGING_AREA_SIZE,
            LocationStates.CHARGING,
        )

    def __str__(self):
        return "\n".join(
            " ".join(str(cell) for cell in row) for row in self.floor_layout
        )
