import shapely.wkt

from _archive.utils.SpeckleDataHandler import SpeckleDataHandler
from _archive.utils.geometries import get_cutter
from _archive.download_data import load_local_data
from _archive.models import Building

level = "02"


def main():
    data = load_local_data("building_data.pkl")
    spek = SpeckleDataHandler(data)
    building = Building()

    spek.process_rooms(building)
    spek.process_doors(building)

    l2 = []
    for room in building.rooms:
        if room.level == level:
            l2.append(room)

    cutter = get_cutter(building, level)

    return


if __name__ == '__main__':
    print(shapely.__version__)
    print(shapely.geos_version)
    main()


