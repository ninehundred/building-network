import csv
import numpy as np
from strip import strip
from make_nwx_point_dict import make_nwx_point_dict


def nwx_node_dict(csv_input_file, node_output_name):
    """
    converts csv file into an nwx compatible dict (each csv line = 1 polygon)
    """
    # TODO: make it so that data incoming is first index of each row is list of points
    # Open csv file
    with open(csv_input_file) as csv_file:
        csv_reader = csv.reader(csv_file)
        # Create np array, strip down to coordinates only for each shape
        pgon_pt_list = np.array([[strip(x) for x in line] for line in csv_reader])
        # Make into 3D array so each shape is a 2D array and so each point is 1D array
        reshape = np.array([np.reshape(x, (-1,3)) for x in pgon_pt_list])
        # Make this shape into a dict with a unique key then return for input into nwx graph
        return [make_nwx_point_dict(shapes, node_output_name) for shapes in reshape]
