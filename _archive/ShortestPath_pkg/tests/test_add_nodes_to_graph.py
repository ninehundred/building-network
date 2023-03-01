""" EXTERNAL MODULES """
import sys
sys.path.append('C:/Users/daniel.odowd/OneDrive - Arup/DO_Documents/SoftwareDevelopment/ShortestPath/ShortestPath/ShortestPath_pkg')
import unittest
import networkx as nx


""" INTERNAL MODULES """
from add_nodes_to_graph import new_add_nodes_to_graph


class TestAddNodesToGraph(unittest.TestCase):
    
    def test_takes_graph_as_arg(self):
        # confirms that we can convert JSON to nwx format
        test_graph = nx.Graph()
        json_file = './data-input/test-data/test_room-data.json'
        new_add_nodes_to_graph(test_graph, json_file)

        # test 1 - graph now has nodes
        self.assertEqual(len(test_graph.nodes()) > 0, True)

        # test 2 - each node has a property called 'pos' with min 2 coordinates
        for node in test_graph.nodes(data = True):
            #print(node[1]['pos'])
            self.assertEqual(len(node[1]['pos']), 2)

        # test 3 - graph has minimum 3 other parameters - room name, room number, room area ...??



# python -m unittest >>> this doesnt seem to work
# python -m unittest test_add_nodes_to_graph.py >>> this does work but only when im in the same folder?
# python -m unittest discover -s tests >>> use this when sitting outside the directory
# note that by default only tests who have test as a prefix will be run. oops!