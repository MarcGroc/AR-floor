from enum import Enum


class Directions(Enum):

    """Robot move directions"""
    NORTH = [-1, 0]
    SOUTH = [+1, 0]
    EAST = [0, +1]
    WEST = [0, -1]
