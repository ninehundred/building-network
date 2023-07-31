from matplotlib import pyplot as plt
from shapely import MultiPolygon, Polygon

from lib.utils.download_data import load_local_data
from lib.utils import plot_any
from lib.utils.SpeckleDataHandler import SpeckleDataHandler
from lib.models import Building, Door
import networkx as nx
from oo_test import calculate_distance
from lib.utils.geometries import construct_cutter


def find_intersecting_doors(room: Polygon, doors: list[Door], level: str) -> list[Door]:
    intersecting_doors = []
    count =0
    for door in doors:
        if door.level == level:
            if room.intersects(door.polygon):
                intersecting_doors.append(door)
                count += 1
            if count > 1:
                break
    return intersecting_doors


def main():
    level = "01"
    test_room = "17"
    data = load_local_data("../examples/building_data.pkl")
    spek = SpeckleDataHandler(data)
    building = Building()

    spek.process_rooms(building)
    spek.process_doors(building)


    graph = nx.Graph()

    for door in enumerate(building.doors):
        if door[1].level == level:
            print("see doors", door[1].id, door[1].level)
            graph.add_node(str(door[0]), pos=door[1].centroid, type=door[1].type, color="yellow", label=door[1].id)
            graph.add_node(str(door[0]) + "upper", pos=door[1].upper_centroid, type=door[1].type, color="yellow", label=door[1].id)
            graph.add_node(str(door[0]) + "lower", pos=door[1].lower_centroid, type=door[1].type, color="yellow", label=door[1].id)

    # get the furthest node from door
    for room in enumerate(building.rooms):
        if room[1].level == level and room[1].number == test_room:
            intersecting_doors = find_intersecting_doors(room[1].polygon, building.doors, level=level)
            print(len(intersecting_doors))
            for x in intersecting_doors:
                print(x.level, x.id)

            maxes = [-1.0, "node"]
            # add coordinates of room to network graph
            print(len(room[1].coordinates))
            for coordinate in enumerate(room[1].coordinates):
                for intersecting_door in intersecting_doors:
                    distance = calculate_distance(coordinate[1], intersecting_door.centroid)
                    print(distance, maxes)
                    if distance > maxes[0]:
                        maxes[0] = distance
                        maxes[1] = str(room[1].number) + str(coordinate[0])
                    graph.add_node(str(room[1].number) + str(coordinate[0]), pos=(coordinate[1]), id=room[1].number, start=False, color="green", distance=distance)
            graph.nodes[maxes[1]]["color"] = "Red"



    cutter = construct_cutter(building, level)

    rooms = []
    for room in building.rooms:
        if room.level == level:
            rooms.append(room.polygon)
    layout = MultiPolygon(rooms)
    plot_any(layout, plt)

    for node in graph.nodes(data=True):
        print(node)

    # labels = nx.get_node_attributes(graph, "label")

    labels = {}
    for node in graph.nodes(data=True):
        id = node[0]
        dx = ""
        if "distance" in node[1]:
            dx = str(node[1]["distance"])
        labels[str(id)] = str(id) + "\n" + str(dx)

    colors = nx.get_node_attributes(graph, "color").values()
    pos = nx.get_node_attributes(graph, 'pos')

    nx.draw(graph, pos, nodelist=graph.nodes(), node_color=colors, labels=labels)
    plt.show()
    return


if __name__ == '__main__':
    main()
