import shapely.affinity
from shapely import Point

from lib.models.Building import Building, Room, Door
from shapely import Polygon


class SpeckleDataHandler:
    door_tolerance = 10

    # temporary measure to identify stair-well doors until speckle can load door data
    # these are the elementId parameters
    # needs a way of identifying door type
    # 
    exit_doors = {"936092", "935699", "935389", "934706"}

    def __init__(self, data):
        self.data = data
        self.rooms = self.data["@Rooms"]
        self.doors = self.data["@Doors"]

    def process_levels(self, building:Building):
        for room in self.data["@Rooms"]:
            # print(x['level'].__dict__)
            # print(room.level.parameters.__dict__)
            # print()
            level_id = room.level.id
            print(level_id)
            level_name = room.name
            level_elevation = room.level.elevation
            # if any of the levels in the buildings level list have the level ID that is about to be added then move on
            # print(f'about to check if there are any levels in the dict...\n{building.levels}')
            # if level_id in building.levels:
            #     print(f'this level {level_id} already exists, moving on...')
            # else:
            #     print('this level does not exist, adding id and level dataclass...')
    


        # get the rooms
        # get the unique level info for all the rooms (so need to check if level already exists)
        # for each unique level id create a level 
        

    def process_doors(self, building: Building):
        for door in self.doors:

            # flatten x,y,z data to get door perimeter
            coordinates = []
            x = door.basePoint.x
            y = door.basePoint.y
            z = door.basePoint.z
            width = door.parameters.FURNITURE_WIDTH.value
            # XXX: we need to get the host wall ID also and its thickness
            # which means we need to import the wall data too
            depth = 120
            offset = width/2

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

            # XXX: need function here to check if there is anything to do with fire exit (some kind of fuzzy search?)
            # XXX: OR the door should be an exit if it has a stair as one of its adjacent rooms
            _type = "norm"
            if door["elementId"] in self.exit_doors:
                _type = "exit"

            polygon = Polygon(coordinates)
            polygon = shapely.affinity.rotate(polygon, door.rotation, use_radians=True, origin='centroid')

            building.doors.append(
                Door(
                    coordinates=coordinates,
                    # XXX: this should be the level ID to ensure we're associated with the correct level
                    level=door.level.name,
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
            coordinates = []
            segments = room.outline['segments']
            for n, segment in enumerate(segments):
                coordinates.append([segment.start.x, segment.start.y])

            polygon = Polygon(coordinates)
            cntrd = polygon.centroid
            centroid = [cntrd.x, cntrd.y]
            building.rooms.append(
                Room(
                    # room_id= TODO: get the room ID from speckle - should be some sort of GUID
                    coordinates=coordinates,
                    centroid=centroid,
                    number=room.number,
                    level=room.level.name,
                    polygon=polygon
                )
            )
        