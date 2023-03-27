# TODO: update entire module to main function on completion
# some sort of universally importable file (web, csv, maybe SQL?)
# TODO: Add unit testing.

from matplotlib import pyplot as plt
# import numpy as np
# import csv
# import itertools
# import math
import networkx as nx
# import time

"""MY MODULES"""
# from add_nodes_to_graph import add_nodes_to_graph
from add_nodes_to_graph import new_add_nodes_to_graph
# from edgeloops import make_continuous_path
from edgeloops import edgeloop_from_graph_points
# from add_start_nodes import add_start_nodes_to_graph
from weighted_edge_generator import weighted_edge_generator
from remove_clashing_edges import remove_clashing_edges


output_graphfile ='test_graph.graph'
# boundary_points_file should contain: csv of pointss
#   each new row should be a new shape.g
boundary_points_file = 'data-input/dev-data/BoundaryPoints'
connective_points_file = 'data-input/dev-data/connectiongraphpoints'
room_exit_points_file = 'data-input/dev-data/RoomExitPoints'
room_boundary_points_file = 'data-input/dev-data/RoomBoundaryPoints'
final_exit_points_file = 'data-input/dev-data/FinalExitPoints'

#boundary_json = 'data-input/dev-data/boundary-data.json'
rooms_json = 'data-input/dev-data/room-data-02.json'
doors_json = 'data-input/dev-data/door-data-03.json'


def main():
    # """NWX GRAPH 1 - BOUNDARY GRAPH"""
    # bdry_g = nx.Graph()
    # # add nodes into boundary graph from file
    # new_add_nodes_to_graph(bdry_g, boundary_json)
    # edgeloop_from_graph_points(bdry_g)
    # # below just makes coordinates for printing
    # bdry_g_node_pos = {node[0] : node[1]['pos'] for node in bdry_g.nodes(data=True)}
    # #bdry_g_node_pos = {node[0] : (node[1]['pos'][0], node[1]['pos'][1])  for node in bdry_g.nodes(data=True)}


    # #bdry_g.add_edges_from(make_edgeloop(bdry_g_node_pos))


    """NWX GRAPH 2 - INTERCONNECTIVITY GRAPH"""
    # create graph - TODO - update this to a class instance later.
    con_g = nx.Graph()
    # add boundary connectivity nodes
    new_add_nodes_to_graph(con_g, rooms_json)
    new_add_nodes_to_graph(con_g, doors_json)

    con_g_node_pos = {node[0] : node[1]['pos'] for node in con_g.nodes(data=True)}
    # Add weighted edges to graph so that lengths are accurate for dijkstra
    weighted_edge_generator(con_g)

    """GRAPH INTERSECTION - I.E. COOKIE CUTTER FUNCTION"""
    # TODO - fix remove clashing edges, currently works with old boundary and old file
    # Removes clashing edges to give ray trace graph
    remove_clashing_edges(con_g, boundary_points_file)


    
    # """FIND SHORTEST PATHS WITH NWX DIJKSTRA ALGORITHM"""
    # # TODO - this can probably be turned into another function
    # start_nodes = []
    # for node in con_g.nodes(data=True):
    #     if "start" in node[0]:
    #         start_nodes.append(node)

    # end_nodes = []
    # for node in con_g.nodes(data=True):
    #     if "fin-exit" in node[0]:
    #         end_nodes.append(node)
    # start_end_products = []
    # start_end_products.append(itertools.product(start_nodes, end_nodes))

    # # TODO: add a function here to check which algorithm to run?
    # path_nodes = []
    # for x in start_end_products:
    #     for y in x:
    #         #pass
    #         try:
    #             path_nodes.append(nx.dijkstra_path(con_g, y[0][0], y[1][0], weight = 'length'))
    #             # TODO: this length needs to get printed somewhere, schedule maybe?
    #             #print(nx.dijkstra_path_length(con_g, y[0][0], y[1][0], weight = 'length'))
    #             #path_nodes.append(nx.shortest_path(con_g, y[0][0], y[1][0]))
    #             #path_nodes.append(nx.astar_path(con_g, y[0][0], y[1][0]))
    #             #path_nodes.append(nx.bellman_ford_path(con_g, y[0][0], y[1][0], weight = 'length'))
    #         except:
    #             print("no path possible")
    

    # TODO: should we make the below into a class so we can just call it with
    # different settings?
    """ PREVIEW DRAW GRAPHS """
    boundary_draw_options = {
        'node_color': 'blue',
        'node_size': 5,
        'node_shape' : 'x',
        'width': 2,
        }
    interconection_draw_options = {
        'node_color': 'red',
        'node_size': 1,
        'node_shape' : 'x',
        'width': 0.1,
        'style': 'dashed',
        }
    path_draw_options = {
        'node_color': 'green',
        'node_size': 1,
        'width': 2,
        'edge_color' : 'r',
        'edge_width' : 1,
        }

    #draw boundary
    nx.draw(bdry_g, bdry_g_node_pos, **boundary_draw_options)
    #draw interconnection graph
    nx.draw(con_g, con_g_node_pos, **interconection_draw_options)

    # draw shortest pathss
    # for items in path_nodes:
    #     #print(items)
    #     path_edges = make_continuous_path(items)
    #     #print(f"PATH EDGES\n{path_edges}")
    #     #nx.draw(con_g, con_g_node_pos,edgelist=path_edges, **path_draw_options)
    #     #weight = nx.get_edge_attributes(con_g, 'weight')

    
    plt.show()

if __name__ == "__main__":
    main()
