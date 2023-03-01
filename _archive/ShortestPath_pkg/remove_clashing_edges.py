import time
import csv
import numpy as np
from strip import strip
from shapely import geometry
from shapely.geometry import LineString
from matplotlib import pyplot as plt

def remove_clashing_edges(conection_graph, boundary_csv):
    """ takes two graphs and removes intersecting edges using naive algorithm"""
    boundary_start_time = time.time()

    shape_out = []
    with open(boundary_csv) as csv_file:
        csv_reader = csv.reader(csv_file)
        # Create np array, strip down to coordinates only for each shape
        pgon_pt_list = np.array([[strip(x) for x in line] for line in csv_reader])

        for shape in pgon_pt_list:
            edge_points = []
            point_1 = 0
            point_2 = 1
            while point_2 < len(shape):
                edge_points.append((float(shape[point_1]), float(shape[point_2])))
                point_1 += 3
                point_2 += 3
            shape_out.append(edge_points)


    polygons = [geometry.Polygon(x) for x in shape_out]

    print(f" BOUNDARY BUILDER RUNTIME = {time.time() - boundary_start_time}")

    reduction_start_time = time.time()
    for c_edge in conection_graph.edges():
        #print(f"checking edge {c_edge}")
        #print(f"here are the coordinates\n {conection_graph.nodes[c_edge[0]]['pos']}")
        l1_p1_x, l1_p1_y = next(iter([conection_graph.nodes[c_edge[0]]['pos']]))
        l1_p2_x, l1_p2_y = next(iter([conection_graph.nodes[c_edge[1]]['pos']]))
        #translate the edge points into shapely geometry
        point1 = geometry.Point(l1_p1_x, l1_p1_y)
        point2 = geometry.Point(l1_p2_x, l1_p2_y)
        con_line = LineString([point1, point2])

        #polygon_shape.contains(point)
        #if our new polygon contains both the points do nothing
        for polys in polygons:
            if polys.exterior.intersects(con_line):
                try:
                    conection_graph.remove_edge(c_edge[0], c_edge[1])
                except:
                    pass
            else:
                pass


    print(f" GRAPH REDUCTION RUNTIME = {time.time() - reduction_start_time}")
