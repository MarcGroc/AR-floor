from pydantic import PositiveInt


class FloorLocaion:
    def __init__(self, x_axis: PositiveInt, y_axis: PositiveInt):
        self.x_axis = x_axis
        self.y_axis = y_axis

