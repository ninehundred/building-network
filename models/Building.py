from dataclasses import dataclass, field
from shapely import Polygon


@dataclass
class Room:
    coordinates: []
    centroid: []
    number: str = ''
    level: str = ''
    polygon: Polygon = Polygon()
    start: bool = False

    # def __init__(self, coordinates, level, id):
    #     self.coordinates = coordinates
    #     self.level = level
    #     self.id = id


@dataclass
class Door:
    coordinates: []
    centroid: list = field(default_factory=list)
    upper_centroid: list = field(default_factory=list)
    lower_centroid: list = field(default_factory=list)
    id: str = ''
    level: str = ''
    rotation: float = 0.0
    room: str = field(default_factory=set)
    type: str = 'norm'
    polygon: Polygon = Polygon()


@dataclass
class Floor:
    Rooms: list[Room]
    id: str = ''


@dataclass
class Building:
    floors: list[Floor] = field(default_factory=set)
    rooms: list[Room] = field(default_factory=list)
    id: str = ''
    doors: list[Door] = field(default_factory=list)
