from dataclasses import dataclass, field
from shapely import Polygon


@dataclass
class Room:
    coordinates: field(default_factory=list)
    centroid: field(default_factory=list)
    room_id: str = ''
    number: str = ''
    level: str = ''
    polygon: Polygon = Polygon()
    start: bool = False


@dataclass
class Door:
    coordinates: field(default_factory=list)
    centroid: list = field(default_factory=list)
    upper_centroid: list = field(default_factory=list)
    lower_centroid: list = field(default_factory=list)
    # XXX: this should be a GUID
    room: str = field(default_factory=set)
    # XXX: This should also be a GUID to associate to the correct level
    level: str = ''
    rotation: float = 0.0
    # TODO: add adjacent room id's so that we can associate the door properly
    type: str = ''
    polygon: Polygon = Polygon()
    id: str = ''

# WIP: renamed to Level as floor is an object that should be associated with a level
@dataclass
class Level:
    #  WIP: added the room dataclass and the doors dataclass to the floor dataclass
    #   for better heirarchical structure of the over all dataclass
    level_id: str = field(default_factory=str)
    level_name: str = field(default_factory=str)
    level_elevation: str = field(default_factory=str)
    rooms: list[Room] = field(default_factory=list) 
    doors: list[Door] = field(default_factory=list)
    id: str = ''


@dataclass
class Building:
    # WIP: updated floors instance variable to a dict containing a 
    #  string of the floor id and then the floor object itself
    #  NOTE: the floor id should be a string represented by a GUID
    levels: dict[str, Level] = field(default_factory=dict)
    id: str = ''
    
