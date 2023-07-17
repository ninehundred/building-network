import shapely.affinity
from shapely import Point

from _archive.models import Building, Room, Door
from shapely import Polygon


class SpeckleDataHandler:
    data: []
    rooms: []
    door_tolerance = 10

    # temporary measure to identify stair-well doors until speckle can load door data
    # these are the elementId parameters
    exit_doors = {"936092", "935699", "935389", "934706"}

    def __init__(self, data):
        # pp = pprint.PrettyPrinter(indent=2)
        self.data = data
        self.rooms = self.data["@Rooms"]
        self.doors = self.data["@Doors"]

    def process_doors(self, building: Building):
        for door in self.doors:

            coordinates = []
            x = door.basePoint.x
            y = door.basePoint.y
            width = door.parameters.FURNITURE_WIDTH.value
            depth = 120
            offset = width/2

            coordinates.append([x-offset, y-depth])
            coordinates.append([x+offset, y-depth])
            coordinates.append([x+offset, y+depth])
            coordinates.append([x-offset, y+depth])

            upper_centroid = Point([x, y+depth])
            lower_centroid = Point([x, y-depth])

            upper_centroid = shapely.affinity.rotate(upper_centroid, door.rotation, use_radians=True, origin=(x, y))
            lower_centroid = shapely.affinity.rotate(lower_centroid, door.rotation, use_radians=True, origin=(x, y))

            _type = "norm"
            if door["elementId"] in self.exit_doors:
                _type = "exit"

            building.doors.append(
                Door(
                    coordinates=coordinates,
                    level=door.level.name,
                    rotation=door.rotation,
                    centroid=[x, y],
                    type=_type,
                    polygon=Polygon(coordinates),
                    upper_centroid=[upper_centroid.x, upper_centroid.y],
                    lower_centroid=[lower_centroid.x, lower_centroid.y]

                )
            )

    def process_rooms(self, building: Building):
        for room in self.rooms:
            coordinates = []
            segments = room.outline['segments']
            for n, segment in enumerate(segments):
                coordinates.append([segment.start.x, segment.start.y])

            polygon = Polygon(coordinates)
            cntrd = polygon.centroid
            centroid = [cntrd.x, cntrd.y]
            building.rooms.append(
                Room(
                    level=room.level.name,
                    coordinates=coordinates,
                    number=room.number,
                    polygon=polygon,
                    centroid=centroid
                )
            )

    def process_floors(self, building: Building):
        return
