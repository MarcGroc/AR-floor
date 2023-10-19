from enum import Enum


class Neighbours(Enum):
    """ Neighbours of a location """
    UP: list[int, int] = [-1, 0]
    DOWN: list[int, int] = [1, 0]
    RIGHT: list[int, int] = [0, 1]
    LEFT: list[int, int] = [0, -1]
