from enum import Enum


class LocationStates(Enum):
    """ Location states, describing purpose of a location"""
    NOT_USED: int = 0
    STORING: int = 1
    PATH: int = 2
    WAITING: int = 3
    PICKING: int = 4
    STOWING: int = 5
    CHARGING: int = 6
