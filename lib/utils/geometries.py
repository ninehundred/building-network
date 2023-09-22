import shapely
from shapely import Polygon, unary_union
import shapely.affinity
from lib.models import Building
from lib.models.Building import Level


def build_polygons(building: Building, floor_label: str):
    doors = []
    rooms = []
    for room in building.rooms:
        if room.level == floor_label:
            poly = Polygon(room.coordinates)
            rooms.append(poly)
            room.polygon = poly

    for door in building.doors:
        if door.level == floor_label:
            poly = Polygon(door.coordinates)
            poly = shapely.affinity.rotate(poly, door.rotation, use_radians=True, origin='centroid')
            doors.append(poly)
            door.polygon = poly
    return doors, rooms


def get_cutter(doors: list[Polygon], rooms: list[Polygon]):

    un_rm = unary_union(rooms)
    un_dr = unary_union(doors)

    return unary_union([un_rm, un_dr])


def construct_cutter(building: Building, floor_label: str):
    # XXX: should a cutter object be created and cached for each level instead of one level at a time?
    doors = []
    rooms = []

    # get the level whose ID matches the incoming ID

    for room in building.rooms:
        if room.level == floor_label:
            rooms.append(room.polygon)

    for door in building.doors:
        if door.level == floor_label:
            doors.append(door.polygon)

    un_rm = unary_union(rooms)
    un_dr = unary_union(doors)
    un = unary_union([un_rm, un_dr])

    return un


def construct_level_cutter(level: Level):
    # XXX: should a cutter object be created and cached for each level instead of one level at a time?
    doors = []
    rooms = []

    # get the level whose ID matches the incoming ID
    for room in level.rooms:
        rooms.append(room.polygon)

    for door in level.doors:
        doors.append(door.polygon)

    un_rm = unary_union(rooms)
    un_dr = unary_union(doors)
    un = unary_union([un_rm, un_dr])

    return un
