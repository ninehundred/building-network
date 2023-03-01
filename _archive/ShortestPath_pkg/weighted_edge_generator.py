import itertools
from get_length import get_segment_len

def weighted_edge_generator(graph):
    """add weighted edges to graph input"""
    for nodepair in itertools.combinations(graph.nodes(data=True), 2):
        graph.add_weighted_edges_from([(nodepair[0][0], nodepair[1][0],
                                 get_segment_len(nodepair[0][1]['pos'][0],
                                 nodepair[0][1]['pos'][1],
                                 nodepair[1][1]['pos'][0],
                                 nodepair[1][1]['pos'][1],
                                 ))], weight='length')
