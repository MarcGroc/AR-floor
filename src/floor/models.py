from sqlalchemy import Column, Integer, UUID
from src.database.base import ArFloorBase


class FloorLocation(ArFloorBase):
    __tablename__ = "floor_location"
    id = Column(UUID, primary_key=True)
    x_axis = Column(Integer)
    y_axis = Column(Integer)


