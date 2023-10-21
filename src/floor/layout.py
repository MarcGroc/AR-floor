from typing import Optional

from pydantic import PositiveInt

from src.config.directions import Directions
from src.config.states import LocationStates
from src.config.areas import FloorAreas
from src.floor.location import Location
from src.floor.constants import *


class FloorLayout:
    """Creates floor layout and assign Location to each cell"""

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
        self._initialize_cells_to_not_used()
        self._initialize_shelve_storing_areas()
        self._initialize_waiting_areas()
        self._initialize_charging_area()
        self._initialize_picking_and_stowing_areas()
        self._initialize_paths()

    def _assign_purpose_to_cells(
        self,
        row_start: int,
        row_end: int | None,
        col_start: int,
        col_end: int | None,
        purpose: LocationStates,
        filter_purpose: Optional[LocationStates] = None,
        heading: Optional[Directions] = None,
    ) -> None:
        for row in self.floor_layout[row_start:row_end]:
            for cell in row[col_start:col_end]:
                self._update_cell(cell, purpose, heading, filter_purpose)

    def _update_cell(self, cell: Location, purpose: LocationStates, heading: Directions, filter_purpose: Optional[LocationStates] = None) -> None:
        if filter_purpose is not None and cell.purpose != filter_purpose:
            return
        cell.purpose = purpose
        if heading:
            cell.heading = heading

    def _initialize_cells_to_not_used(self) -> None:
        self._assign_purpose_to_cells(
            INITIAL_ROW_COL,
            self._x_axis,
            INITIAL_ROW_COL,
            self._y_axis,
            LocationStates.NOT_USED,
            filter_purpose=None,
        )

    def _initialize_shelve_storing_areas(self) -> None:
        self._assign_purpose_to_cells(
            FloorAreas.INNER_FLOOR.value,
            self._y_axis - FloorAreas.INNER_FLOOR.value,
            FloorAreas.INNER_FLOOR.value,
            self._y_axis - FloorAreas.INNER_FLOOR.value,
            LocationStates.STORING,
        )

    def _initialize_waiting_areas(self) -> None:
        # Top horizontal
        self._assign_purpose_to_cells(
            FloorAreas.INITIAL_WAITING_LINE.value,
            FloorAreas.OUTER_FLOOR.value,
            FloorAreas.INITIAL_WAITING_LINE.value,
            self._x_axis - FloorAreas.INITIAL_WAITING_LINE.value,
            LocationStates.WAITING,
        )

        # Bottom horizontal
        self._assign_purpose_to_cells(
            self._x_axis - FloorAreas.OUTER_FLOOR.value,
            -FloorAreas.INITIAL_WAITING_LINE.value,
            FloorAreas.INITIAL_WAITING_LINE.value,
            self._x_axis - FloorAreas.INITIAL_WAITING_LINE.value,
            LocationStates.WAITING,
        )

        # Vertical - Left
        self._assign_purpose_to_cells(
            FloorAreas.INITIAL_WAITING_LINE.value,
            -FloorAreas.INITIAL_WAITING_LINE.value,
            FloorAreas.INITIAL_WAITING_LINE.value,
            FloorAreas.OUTER_FLOOR.value,
            LocationStates.WAITING,
        )

        # Vertical - Right
        self._assign_purpose_to_cells(
            FloorAreas.INITIAL_WAITING_LINE.value,
            -FloorAreas.INITIAL_WAITING_LINE.value,
            self._y_axis - FloorAreas.OUTER_FLOOR.value,
            self._y_axis - FloorAreas.INITIAL_WAITING_LINE.value,
            LocationStates.WAITING,
        )

    def _initialize_picking_and_stowing_areas(self) -> None:
        filter_purpose = (
            LocationStates.NOT_USED
        )  # Cells to be overwritten must be NOT_TAKEN

        for cell in range(
            INITIAL_PICKING_WORKSTATION,
            self._x_axis - INITIAL_WORKSTATION,
            WORKSTATION_GAP,
        ):
            self._assign_purpose_to_cells(
                INITIAL_ROW_COL,
                END_ROW_COL,
                cell,
                cell + END_ROW_COL,
                LocationStates.PICKING,
                filter_purpose,
                Directions.NORTH,
            )
            self._assign_purpose_to_cells(
                -END_ROW_COL,
                None,
                cell,
                cell + END_ROW_COL,
                LocationStates.PICKING,
                filter_purpose,
                Directions.SOUTH,
            )

        for cell in range(
            INITIAL_STOWING_WORKSTATION,
            self._x_axis - INITIAL_WORKSTATION,
            WORKSTATION_GAP,
        ):
            self._assign_purpose_to_cells(
                INITIAL_ROW_COL,
                END_ROW_COL,
                cell,
                cell + END_ROW_COL,
                LocationStates.STOWING,
                filter_purpose,
                Directions.NORTH,
            )
            self._assign_purpose_to_cells(
                -END_ROW_COL,
                None,
                cell,
                cell + END_ROW_COL,
                LocationStates.STOWING,
                filter_purpose,
                Directions.SOUTH,
            )

        for cell in range(
            INITIAL_WORKSTATION, self._y_axis - INITIAL_WORKSTATION, WORKSTATION_GAP
        ):
            self._assign_purpose_to_cells(
                cell,
                cell + END_ROW_COL,
                INITIAL_ROW_COL,
                END_ROW_COL,
                LocationStates.PICKING,
                filter_purpose,
                Directions.WEST,
            )
            self._assign_purpose_to_cells(
                cell,
                cell + END_ROW_COL,
                -END_ROW_COL,
                None,
                LocationStates.PICKING,
                filter_purpose,
                Directions.EAST,
            )

        for cell in range(
            WORKSTATION_GAP, self._y_axis - INITIAL_WORKSTATION, WORKSTATION_GAP
        ):
            self._assign_purpose_to_cells(
                cell,
                cell + END_ROW_COL,
                INITIAL_ROW_COL,
                END_ROW_COL,
                LocationStates.STOWING,
                filter_purpose,
                Directions.WEST,
            )
            self._assign_purpose_to_cells(
                cell,
                cell + END_ROW_COL,
                -END_ROW_COL,
                None,
                LocationStates.STOWING,
                filter_purpose,
                Directions.EAST,
            )

    def _initialize_paths(self) -> None:
        # Vertical left and right
        self._assign_purpose_to_cells(
            FloorAreas.OUTER_FLOOR.value,
            -FloorAreas.OUTER_FLOOR.value,
            FloorAreas.OUTER_FLOOR.value,
            FloorAreas.INNER_FLOOR.value,
            LocationStates.PATH,
        )
        self._assign_purpose_to_cells(
            FloorAreas.OUTER_FLOOR.value,
            -FloorAreas.OUTER_FLOOR.value,
            self._y_axis - FloorAreas.INNER_FLOOR.value,
            self._y_axis - FloorAreas.OUTER_FLOOR.value,
            LocationStates.PATH,
        )

        # Horizontal top
        self._assign_purpose_to_cells(
            FloorAreas.OUTER_FLOOR.value,
            FloorAreas.INNER_FLOOR.value,
            FloorAreas.INNER_FLOOR.value,
            self._x_axis - FloorAreas.INNER_FLOOR.value,
            LocationStates.PATH,
        )

        # Horizontal bottom
        self._assign_purpose_to_cells(
            self._x_axis - FloorAreas.INNER_FLOOR.value,
            self._x_axis - FloorAreas.OUTER_FLOOR.value,
            FloorAreas.INNER_FLOOR.value,
            self._y_axis - FloorAreas.INNER_FLOOR.value,
            LocationStates.PATH,
        )
        # Aisles vertical
        for col_start in range(
            FloorAreas.INITIAL_AISLE.value,
            self._y_axis - FloorAreas.INNER_FLOOR.value,
            FloorAreas.AISLE_GAP.value,
        ):
            self._assign_purpose_to_cells(
                INITIAL_ROW_COL + END_ROW_COL,
                self._x_axis - END_ROW_COL,
                col_start,
                col_start + END_ROW_COL,
                LocationStates.PATH,
            )

        # Aisles horizontal
        for row_start in range(
            FloorAreas.INITIAL_AISLE.value,
            self._x_axis - FloorAreas.INNER_FLOOR.value,
            FloorAreas.AISLE_GAP.value,
        ):
            self._assign_purpose_to_cells(
                row_start,
                row_start + END_ROW_COL,
                INITIAL_ROW_COL + END_ROW_COL,
                self._y_axis - END_ROW_COL,
                LocationStates.PATH,
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

    def __repr__(self):
        return str(self.floor_layout)
