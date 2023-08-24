import shapely.affinity
from shapely import Point

from lib.models.Building import Building, Room, Door, Level
from shapely import Polygon


class SpeckleDataHandler:
    door_tolerance = 10
    exit_doors = {"936092", "935699", "935389", "934706"}

    def __init__(self, data):
        self.data = data
        self.rooms = self.data["@Rooms"]
        self.doors = self.data["@Doors"]

    def process_levels(self, building:Building):
        for room in self.data["@Rooms"]:
            level_id = room.level.id
            level_name = room.level.name
            level_elevation = room.level.elevation
            if level_id not in building.levels:
                # level does not exist, adding id and level dataclass
                building.levels[level_id] = Level(level_id=level_id, 
                                                  level_name=level_name,
                                                  level_elevation=level_elevation
                                                  )
                
    def process_doors(self, building: Building):

        for door in self.doors:
            # TODO: need to think about how we generate the geometry from the door
            #       this looks like it might need to be some sort of bounding box 
            point_coordinates = [door.displayValue[0].vertices[i:i+3] for i in range(0, len(door.displayValue[0].vertices), 3)]

            # TODO: add facingFlipped and handFlipped as one of the door properties - this could help us figure out which way the door is facing

            # flatten x,y,z data to get door perimeter
            coordinates = []
            x = door.basePoint.x
            y = door.basePoint.y
            z = door.basePoint.z
            width = door.parameters.FURNITURE_WIDTH.value
            # XXX: we need to get the host wall ID also and its thickness
            # which means we need to import the wall data too
            depth = 120 # TODO: this should come from a property of the host wall.
            offset = width/2 #TODO: this should come from a parameter 'clear width'

            # TODO: check if there is a convex hull method
            # XXX: shapely has a convex hull method
            coordinates.append([x-offset, y-depth, z])
            coordinates.append([x+offset, y-depth, z])
            coordinates.append([x+offset, y+depth, z])
            coordinates.append([x-offset, y+depth, z])

            upper_centroid = Point([x, y+depth, z])
            lower_centroid = Point([x, y-depth, z])

            upper_centroid = shapely.affinity.rotate(upper_centroid, door.rotation, use_radians=True, origin=(x, y, z))
            lower_centroid = shapely.affinity.rotate(lower_centroid, door.rotation, use_radians=True, origin=(x, y, z))

            # TODO : add some kind of search to look in the parameters for anything to do with 'exit type'
            #       and replace the _type property below
            _type = "norm"
            if door["elementId"] in self.exit_doors:
                _type = "exit"

            polygon = Polygon(coordinates)
            polygon = shapely.affinity.rotate(polygon, door.rotation, use_radians=True, origin='centroid')


            for level_id in building.levels.keys():
                if door.level.id == level_id:
                    building.levels[door.level.id].doors.append(
                        Door(
                            coordinates=coordinates,
                            level=door.level.id,
                            rotation=door.rotation,
                            centroid=[x, y, z],
                            type=_type,
                            polygon=polygon,
                            upper_centroid=[upper_centroid.x, upper_centroid.y],
                            lower_centroid=[lower_centroid.x, lower_centroid.y]

                        )
                    )

    def process_rooms(self, building: Building):
        for room in self.rooms:
            # TODO: this function needs to be rebuilt to take voids.
            coordinates = []
            segments = room.outline['segments']
            for n, segment in enumerate(segments):
                coordinates.append([segment.start.x, segment.start.y, segment.start.z])
            
            polygon = Polygon(coordinates)
            room_centre_point = [polygon.centroid.x, polygon.centroid.y]
            
            for level_id in building.levels.keys():
                if level_id == room.level.id:
                    building.levels[room.level.id].rooms.append(
                        Room(
                            room_id = room.parameters.id,
                            room_coordinates = coordinates,
                            room_centre_point = room_centre_point,
                            room_number = room.number,
                            associated_level = room.level.id,
                            polygon = polygon
                        )
                    )
    