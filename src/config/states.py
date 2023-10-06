from enum import Enum


class LocationStates(Enum):
    """ Location states """
    NOT_TAKEN = 0
    TAKEN = 1
    ON_PATH = 2
    WAITING = 3
    PICKING = 4
    STOWING = 5
    CHARGING = 6
    STORING = 7
