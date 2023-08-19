from enum import Enum


class FloorLocationStates(Enum):
    """
    Attributes:
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

    NOT_TAKEN = 0
    TAKEN = 1
    ON_PATH = " "
    WAITING = 3
    PICKING = 4
    STOWING = 5
    CHARGING = 6
