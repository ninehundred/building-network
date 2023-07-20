from dataclasses import dataclass, field
from shapely import Polygon


@dataclass
class Room:
    room_id: str = ''
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
    id: str = ''
    coordinates: []
    centroid: list = field(default_factory=list)
    upper_centroid: list = field(default_factory=list)
    lower_centroid: list = field(default_factory=list)
    level: str = ''
    rotation: float = 0.0
    # XXX: is this a set of two room ID's?
    room: str = field(default_factory=set)
    # identify if door leads to a stairwell
    type: str = 'norm'
    polygon: Polygon = Polygon()


@dataclass
class Floor:
    Rooms: list[Room]
    id: str = ''
    """ XXX: why does the floor have room objects as well
        as the building? shouldnt the building have floors,
        and on the floors there are rooms?
    """


@dataclass
class Building:
    # floors should be a dict
    # {"<floor_id>": dict(rooms)}
    id: str = ''
    floors: list[Floor] = field(default_factory=set)
    rooms: list[Room] = field(default_factory=list) 
    doors: list[Door] = field(default_factory=list)
