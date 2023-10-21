from enum import Enum


class Neighbours(Enum):
    """ Neighbours of a location """
    UP: tuple[int, int] = (-1, 0)
    DOWN: tuple[int, int] = (1, 0)
    RIGHT: tuple[int, int] = (0, 1)
    LEFT: tuple[int, int] = (0, -1)
