import shapely.affinity
from shapely import Point

from lib.models.Building import Building, Room, Door
from shapely import Polygon


class SpeckleDataHandler:
    door_tolerance = 10

    # temporary measure to identify stair-well doors until speckle can load door data
    # these are the elementId parameters
    # needs a way of identifying door type
    exit_doors = {"936092", "935699", "935389", "934706"}

    def __init__(self, data):
        # pp = pprint.PrettyPrinter(indent=2)
        self.data = data
        self.rooms = self.data["@Rooms"]
        self.doors = self.data["@Doors"]

    def process_doors(self, building: Building):
        for door in self.doors:

            # flatten x,y,z data to get door perimeter
            coordinates = []
            x = door.basePoint.x
            y = door.basePoint.y
            width = door.parameters.FURNITURE_WIDTH.value
            depth = 120
            offset = width/2

            # TODO check if there is a convex hull method
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

            polygon = Polygon(coordinates)
            polygon = shapely.affinity.rotate(polygon, door.rotation, use_radians=True, origin='centroid')

            building.doors.append(
                Door(
                    coordinates=coordinates,
                    level=door.level.name,
                    rotation=door.rotation,
                    centroid=[x, y],
                    type=_type,
                    polygon=polygon,
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
