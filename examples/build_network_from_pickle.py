import os
import pickle

import networkx as nx
from matplotlib import pyplot as plt

from lib.build_network.BuildLevelNetwork import BuildLevelNetwork
from lib.utils.download_data import load_local_data
from lib.models.Building import Building
from lib.utils.SpeckleDataHandler import SpeckleDataHandler


def main():
    # print(os.listdir())
    with open(r"building_data.pkl", 'rb') as read:
        data = pickle.load(read)

    # todo - OO
    # For each level, identify the room containing the stairs
    # Add centroid to that room
    # after generating the graph for each level, loop through levels and manually join those stair centroids together
    # how do we calculate the distance between each stair centroid?

    # Create a building object class with all required data
    building_01_obj = Building()
    speckle_data_handler = SpeckleDataHandler(data)
    speckle_data_handler.process_levels(building_01_obj)
    speckle_data_handler.process_rooms(building_01_obj)
    speckle_data_handler.process_doors(building_01_obj)

    # XXX: might start looking a bit different from here as the level will need to be an ID.
    # XXX: may have to start looking into a basic front end here to display all level info in drop down menu or something

    building_levels = [level for level in building_01_obj.levels]

    # building_network = BuildLevelNetwork(building=building_01_obj, level="02") #build all levels at once as a single building that we can call functions on each level.
    building_network = dict()
    for level_id, level_obj in building_01_obj.levels.items():
        building_network[level_id] = BuildLevelNetwork(level=building_01_obj.levels[level_id])

    test_level = building_levels[0]
    building_network[test_level].add_door_centroids()
    building_network[test_level].add_room_coordinates()
    building_network[test_level].compute_all_edges()
    building_network[test_level].remove_intersecting_edges()
    building_network[test_level].add_room_centroids()

    for node in building_network[test_level].graph:
        print(node), print(building_network[test_level].graph[node])

    graph = building_network[test_level].graph
    edge_graph = nx.complete_graph(graph)
    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw(graph, pos, nodelist=graph.nodes())
    nx.draw(graph, pos, nodelist=edge_graph.nodes())
    # nx.draw_networkx_edges(graph, pos=pos, edgelist=edge_graph.nodes)
    plt.show()

    ### functions to plot paths on a level or plot paths from elements to element
    # TODO: these functions will be called with a particular level in mind

    # TODO: build this function with a view that we might want to push the lines and points back to speckle
    building_network[test_level].plot_all_paths(normalise=25, exit_node="103")
    # building_network[test_level].plot_single_path(normalise=25, start_node_index=1)
    return


if __name__ == "__main__":
    main()
