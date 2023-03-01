import time
import re

def make_edgeloop(points):
    """
    takes in dict whos keys represent nwx nodes
    returns a list of tuples (edges made of (point, point)) in the order of the
    point values that were supplied e.g. if 1,2,3,4 is supplied we get:
    [(1,2),(2,3),(3,4)] so make sure points are in order!
    """
    #make_edgeloop_start_time = time.time()
    edge_points = []
    point_list = list(points.keys())
    point_1 = 0
    point_2 = 1
    while point_2 < len(point_list):
        edge_points.append((point_list[point_1], point_list[point_2]))
        point_1 += 1
        point_2 += 1
    edge_points.append((point_list[int(len(point_list) -1)], point_list[0]))
    #print(f" MAKE CONTINUOUS EDGE RUNTIME = {time.time() - make_edgeloop_start_time}")
    return edge_points

def edgeloop_from_graph_points(graph):
    """ adds a continous chain of edges around each node in graph from start to finish"""
    # TODO - test? this should test that graphcs with less than 3 nodes do not get through.
    node_list = list(graph.nodes())
    node_dict = {}
    for count, node in enumerate(node_list):
        # if the next number isnt longer than our list of nodes
        if(count + 1 < len(node_list) -1):
            matched_object = re.search('^.*?(?=node+\D)', node)
            # print(matched_object.group(), '<<<<this is the group')
            # print(node_list[count+1])
            # print(matched_object.group() in node_list[count + 1])
            # print()
            # if the key exists already
            if (matched_object.group() in node_dict.keys()):
                # if our dict key is the same as hte next one
                if (matched_object.group() in node_list[count + 1]):
                    node_dict[matched_object.group()].append([(node, node_list[count + 1])])
            # else if our key doesnt already exist
            else:
                # and if the next object doesnt have our key in it
                if (matched_object.group() in node_list[count + 1]):
                    node_dict[matched_object] = [[(node, node_list[count + 1])]]
                    
    for element in node_dict:
        for edge in node_dict[element]:
            graph.add_edges_from(edge)
   


def make_continuous_path(nodes):
    path_points = []
    point_1 = 0
    point_2 = 1
    while point_2 < len(nodes):
        path_points.append((nodes[point_1], nodes[point_2]))
        point_1 += 1
        point_2 += 1
    return path_points
