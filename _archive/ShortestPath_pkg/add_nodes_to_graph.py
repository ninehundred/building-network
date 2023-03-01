""" EXTERNAL MODULES"""
import time
import json
import sys
sys.path.append('C:/Users/daniel.odowd/OneDrive - Arup/DO_Documents/SoftwareDevelopment/ShortestPath/ShortestPath/ShortestPath_pkg')

""" INTERNAL MODULES """
from nwx_node_dict import nwx_node_dict
from edgeloops import make_edgeloop

def add_nodes_to_graph(graph, points_file, node_name):
    add_nodes_start_time = time.time()
    """takes boundary point csv file and adds shapes to graph. points should be
    comma separated while the boundary shapes should be line separated"""
    shapes_list = nwx_node_dict(points_file, node_name)
    for shape in shapes_list:
        for points in shapes_list:
            # Add nodes from list of dict keys
            graph.add_nodes_from(points.keys())
            # Give nodes coordinate points from dict.
            for node, point in points.items():
                #print(point, 'this is what a point looks like')
                graph.nodes[node]['pos'] = point

            graph.add_edges_from(make_edgeloop(points))

    print(f" ADDING NODES RUNTIME = {time.time() - add_nodes_start_time}")

# run in terminal - python -m unittest test_add_nodes_to_graph

def new_add_nodes_to_graph(graph, jsonfile):
    add_nodes_start_time = time.time()
    # open file location
    with open(jsonfile) as jsonfile:
        # then pass the contents of the file to the json loader and convert to dict
        data = json.load(jsonfile)
        # for each element (shape) in the json file
        for element in data.get("features"):
            properties = element.get("properties")
            #print(properties)
            all_coordinates = element.get("geometry").get("coordinates")
            # add each node to the graph with the room number plus sequence value
            for count, coordinate in enumerate(all_coordinates):
                # TODO - need to ensure that the object coming through has a number property
                if (properties.get('Number') != ""):
                    node_name =f"{properties.get('Number')}-node-{count}"
                    graph.add_nodes_from([(node_name, properties)])
                else:
                    node_name = 'door' + str(count)
                    graph.add_nodes_from([(node_name, properties)])
                #print((coordinate[0],coordinate[1]), 'this is what a coordinate looks like')
                graph.nodes[node_name]['pos'] = (float(coordinate[0]), float(coordinate[1]))
    print(f" ADDING NODES RUNTIME = {time.time() - add_nodes_start_time}")

    