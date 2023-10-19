from enum import Enum


class Directions(Enum):

    """Robot move directions and workstation  heading directions"""

    NORTH: int = 0
    SOUTH: int = 1
    EAST: int = 2
    WEST: int = 3
