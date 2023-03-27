import networkx
from matplotlib import pyplot as plt
import networkx as nx
from shapely import LineString

from utils.SpeckleDataHandler import SpeckleDataHandler
from utils.geometries import construct_cutter, build_polygons, get_cutter
from _archive.download_data import load_local_data
from models.Building import Building
from utils.tools import plot_any
import math
import colorsys

'''
this code needs to be refactored into a class/classes
'''

gl = "Origin_Project Datum"
level = "03"


def calculate_distance(u: list, v: list):
    distance = math.sqrt(((u[0] - v[0])**2) + ((u[1] - v[1])**2))
    return distance/1000


def print_edges(_graph):
    for u, v, d in _graph.edges(data=True):
        print(f"({u}, {v}) {d=}")


def print_nodes(_graph):
    for u, d in _graph.nodes(data=True):
        print(u, d)

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))

def main():
    data = load_local_data("building_data.pkl")
    spek = SpeckleDataHandler(data)
    building = Building()

    spek.process_rooms(building)
    spek.process_doors(building)

    graph = nx.Graph()

    exit_nodes = []
    start_nodes = []

    # add door centroid coordinates to graph
    for door in enumerate(building.doors):
        if door[1].level == level:
            graph.add_node(str(door[0]), pos=door[1].centroid, type=door[1].type, color="yellow")
            graph.add_node(str(door[0]) + "upper", pos=door[1].upper_centroid, type=door[1].type, color="yellow")
            graph.add_node(str(door[0]) + "lower", pos=door[1].lower_centroid, type=door[1].type, color="yellow")
            if door[1].type == "exit":
                exit_nodes.append(str(door[0]))

    # add room corners coordinates to graph
    for room in enumerate(building.rooms):
        if room[1].level == level:

            coordinates = room[1].coordinates

            door_centroid = []
            for door in building.doors:
                if door.level == level:
                    if room[1].polygon.intersects(door.polygon):
                        door_centroid.append(door.centroid[0])
                        door_centroid.append(door.centroid[1])
                        break

            # calculate furthest point from door

            curr_distance = 0.0
            furthest_point_index = 0

            for coordinate in enumerate(coordinates):
                distance = calculate_distance(coordinate[1], door_centroid)

                if distance > curr_distance:
                    curr_distance = distance
                    furthest_point_index = coordinate[0]

            for coordinate in enumerate(coordinates):
                if coordinate[0] == furthest_point_index:
                    start_nodes.append(str(room[1].number) + str(coordinate[0]))
                    graph.add_node(str(room[1].number) + str(coordinate[0]), pos=(coordinate[1]), id=room[1].number, start=True, color="green")
                else:
                    graph.add_node(str(room[1].number) + str(coordinate[0]), pos=(coordinate[1]), id=room[1].number, start=False, color="blue")

    cutter = construct_cutter(building, level)
    # doors, rooms = build_polygons(building, level)
    # cutter = get_cutter(rooms, doors)

    g1 = nx.complete_graph(graph)

    plot_any(cutter, plt)
    for inner in cutter.interiors:
        xx, yy = inner.xy
        plt.plot(xx, yy)

    linestrings = []

    # remove intersecting edges
    for edge in g1.edges():
        line = LineString([graph.nodes[edge[0]]["pos"], graph.nodes[edge[1]]["pos"]])
        if line.crosses(cutter):
            g1.remove_edge(edge[0], edge[1])
            continue
        for interior in cutter.interiors:
            if line.crosses(interior):
                g1.remove_edge(edge[0], edge[1])
                continue
        if not cutter.contains(line):
            g1.remove_edge(edge[0], edge[1])

    # add weight to edges
    for edge in g1.edges(data=True):
        u, v, d = edge
        uu = graph.nodes[u]["pos"]
        vv = graph.nodes[v]["pos"]
        weight = calculate_distance(uu, vv)
        g1[u][v]["weight"] = weight


    sn = 4
    tn = 0

    def find_shortest_path(g: nx.Graph, start_nodes: list[str], end_node: str):
        paths = []
        lengths = []
        for node in start_nodes:
            shortest_path = nx.shortest_path(g, source=node, target=end_node, weight='weight')
            shortest_path_length = nx.shortest_path_length(g1, source=node, target=end_node, weight='weight')
            path_edges = list(zip(shortest_path, shortest_path[1:]))
            paths.append(path_edges)
            lengths.append(shortest_path_length)
        return paths, lengths

    for room in enumerate(building.rooms):
        if room[1].level == level:
            graph.add_node(str(room[0]) + "centroid", pos=room[1].centroid, id=room[1].number, start=False, color="Red", label=room[1].number)

    colors = nx.get_node_attributes(graph, "color").values()
    labels = nx.get_node_attributes(graph, "label")
    pos = nx.get_node_attributes(graph, 'pos')

    # nx.draw(g1, pos)
    edges, lengths = find_shortest_path(g1, start_nodes, exit_nodes[0])
    print(len(edges))
    print(len(lengths))
    print(start_nodes)

    ix = 1

    edge = edges[ix]
    length = lengths[ix]

    # for edge in enumerate(edges):
    #     idx = edge[0]
    #     hue = float((lengths[idx]/25))
    #     rgb = colorsys.hsv_to_rgb(hue, 1, 1)
    #     hex = rgb_to_hex(rgb[0], rgb[1], rgb[2])
    #     nx.draw(graph, pos, edgelist=edge[1], edge_color=hex, width=2)
    #
    hue = float(length/30)
    rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    hex = rgb_to_hex(rgb[0], rgb[1], rgb[2])
    nx.draw(graph, pos, edgelist=edge, edge_color=hex, width=2)

    nx.draw(graph, pos, nodelist=graph.nodes(), node_color=colors, labels=labels)

    # pos = nx.get_node_attributes(centroids_graph, 'pos')
    # nx.draw(centroids_graph, pos)

    plt.show()
    return


if __name__ == '__main__':
    # print(shapely.__version__)
    # print(shapely.geos_version)
    main()
