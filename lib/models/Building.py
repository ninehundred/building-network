from dataclasses import dataclass, field
from shapely import Polygon


@dataclass
class Room:
    """
    Dataclass representing the geometry and properties of a room. 
    This object should be placed on a level within a building.
    """
    room_id: str = field(default_factory=str)
    room_coordinates: list = field(default_factory=list)
    room_centre_point: list = field(default_factory=list)
    room_number: str = field(default_factory=str)
    associated_level: str = field(default_factory=str)
    occupancy: int = field(default_factory=int)
    # TODO: fire resistance requirement
    # TODO: ancillary type
    # TODO: risk profile
    # TODO: floor space factor 

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
    """
    Dataclass representing a level on a building. Not to be mistaken with a floor.
    A level hosts various other objects such as rooms and doors.
    """
    level_id: str = field(default_factory=str)
    level_name: str = field(default_factory=str)
    level_elevation: str = field(default_factory=str)
    rooms: list[Room] = field(default_factory=list) 
    doors: list[Door] = field(default_factory=list)
    id: str = ''


@dataclass
class Building:
    """
    Dataclass representing a building. This will host levels.
    """
    levels: dict[str, Level] = field(default_factory=dict)
    id: str = ''
    
