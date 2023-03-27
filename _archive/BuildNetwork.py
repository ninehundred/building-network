import colorsys
import math
from shapely import Polygon, LineString
import networkx as nx
from matplotlib import pyplot as plt

from models.Building import Building, Room, Door
from utils.geometries import construct_cutter
from utils.tools import plot_any


class BuildNetwork:
    building: Building
    graph: nx.Graph
    edge_graph: nx.Graph
    exit_nodes: list
    start_nodes: list
    level: str
    cutter = Polygon

    def __init__(self, building: Building, level: str):
        self.building = building
        self.graph = nx.Graph()
        self.start_nodes = []
        self.exit_nodes = []
        self.level = level
        self.cutter = construct_cutter(building, self.level)

    @staticmethod
    def calculate_distance(u: list, v: list):
        distance = math.sqrt(((u[0] - v[0])**2) + ((u[1] - v[1])**2))
        return distance/1000

    @staticmethod
    def rgb_to_hex(r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))

    def get_hex_color(self, length: float, normalize: float):
        hue = float(length/30)
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        return self.rgb_to_hex(rgb[0], rgb[1], rgb[2])

    def add_door_centroids(self):
        for door in enumerate(self.building.doors):
            if door[1].level == self.level:
                self.graph.add_node(str(door[0]), pos=door[1].centroid, type=door[1].type, color="yellow")
                self.graph.add_node(str(door[0]) + "upper", pos=door[1].upper_centroid, type=door[1].type,
                                    color="yellow")
                self.graph.add_node(str(door[0]) + "lower", pos=door[1].lower_centroid, type=door[1].type,
                                    color="yellow")
                if door[1].type == "exit":
                    self.exit_nodes.append(str(door[0]))

    def get_furthest_node_from_door(self, room: Room, intersecting_doors: list):
        maxes = [-1.0, "node"]
        for coordinate in enumerate(room.coordinates):
            for intersecting_door in intersecting_doors:
                distance = self.calculate_distance(coordinate[1], intersecting_door.centroid)
                if distance > maxes[0]:
                    maxes[0] = distance
                    maxes[1] = str(room.number) + str(coordinate[0])
        return maxes[1]

    def add_room_coordinates(self):
        for room in enumerate(self.building.rooms):
            if room[1].level == self.level:
                coordinates = room[1].coordinates
                intersecting_doors = self.find_intersecting_doors(room[1].polygon)
                furthest_node = self.get_furthest_node_from_door(room[1], intersecting_doors)
                for coordinate in enumerate(coordinates):
                    name = str(room[1].number) + str(coordinate[0])
                    if name == furthest_node:
                        self.start_nodes.append(str(room[1].number) + str(coordinate[0]))
                        self.graph.add_node(str(room[1].number) + str(coordinate[0]), pos=(coordinate[1]), id=room[1].number, start=True, color="green")
                    else:
                        self.graph.add_node(str(room[1].number) + str(coordinate[0]), pos=(coordinate[1]), id=room[1].number, start=False, color="blue")

    # this is just for labelling, and should be called after all edges have been drawn
    # if called before edges are drawn, the path from the room will go through the centroid
    def add_room_centroids(self):
        for room in enumerate(self.building.rooms):
            if room[1].level == self.level:
                self.graph.add_node(str(room[0]) + "centroid", pos=room[1].centroid, id=room[1].number, start=False, color="Red", label=room[1].number)

    def find_intersecting_doors(self, room: Polygon) -> list[Door]:
        doors = self.building.doors
        intersecting_doors = []
        count = 0
        for door in doors:
            if door.level == self.level:
                if room.intersects(door.polygon):
                    intersecting_doors.append(door)
                    count += 1
                if count > 1:
                    break
        return intersecting_doors

    def compute_all_edges(self):
        self.edge_graph = nx.complete_graph(self.graph)

    def remove_intersecting_edges(self):
        for edge in self.edge_graph.edges():
            line = LineString([self.graph.nodes[edge[0]]["pos"], self.graph.nodes[edge[1]]["pos"]])
            if line.crosses(self.cutter):
                self.edge_graph.remove_edge(edge[0], edge[1])
                continue
            for interior in self.cutter.interiors:
                if line.crosses(interior):
                    self.edge_graph.remove_edge(edge[0], edge[1])
                    continue
            if not self.cutter.contains(line):
                self.edge_graph.remove_edge(edge[0], edge[1])

    def find_shortest_paths(self):
        paths = []
        lengths = []
        self.compute_all_edges()
        self.remove_intersecting_edges()
        for node in self.start_nodes:
            shortest_path = nx.shortest_path(self.edge_graph, source=node, target=self.exit_nodes[0], weight='weight')
            shortest_path_length = nx.shortest_path_length(self.edge_graph, source=node, target=self.exit_nodes[0], weight='weight')
            path_edges = list(zip(shortest_path, shortest_path[1:]))
            paths.append(path_edges)
            lengths.append(shortest_path_length)
        return paths, lengths

    def plot_all_paths(self):
        colors = nx.get_node_attributes(self.graph, "color").values()
        labels = nx.get_node_attributes(self.graph, "label")
        pos = nx.get_node_attributes(self.graph, 'pos')
        edges, lengths = self.find_shortest_paths()
        plot_any(self.cutter, plt)

        for edge, length in zip(edges, lengths):
            hue = float(length/25)
            rgb = colorsys.hsv_to_rgb(hue, 1, 1)
            hex_clr = self.rgb_to_hex(rgb[0], rgb[1], rgb[2])
            nx.draw(self.graph, pos, edgelist=edge, edge_color=hex_clr, width=2)
        nx.draw(self.graph, pos, nodelist=self.graph.nodes(), node_color=colors, labels=labels)
        plt.show()

    def plot_single_path(self, start_node_index: int = 0):
        colors = nx.get_node_attributes(self.graph, "color").values()
        labels = nx.get_node_attributes(self.graph, "label")

        pos = nx.get_node_attributes(self.graph, 'pos')
        edges, lengths = self.find_shortest_paths()

        hex_clr = self.get_hex_color(lengths[start_node_index], 30.0)
        plot_any(self.cutter, plt)
        nx.draw(self.graph, pos, edgelist=edges[start_node_index], edge_color=hex_clr, width=2)
        nx.draw(self.graph, pos, nodelist=self.graph.nodes(), node_color=colors, labels=labels)
        plt.show()
        return
