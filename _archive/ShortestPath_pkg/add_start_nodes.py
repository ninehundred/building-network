from nwx_node_dict import nwx_node_dict
import itertools
from get_length import get_segment_len

def add_start_nodes_to_graph(graph, room_exit_points_file, room_boundary_points_file):
    """
    takes in two csv files. each room on new line, each rm exit on new line
    pairs up room with room exit so must be in order in each csv file
    """
    # NOTE: I think this may only work if the room has one exit door
    room_exit_dicts = nwx_node_dict(room_exit_points_file, "rm-exit")
    room_points_dicts = nwx_node_dict(room_boundary_points_file, "start")

    rm_to_rm_boundary_pts = []
    for exits, rooms in zip(room_exit_dicts, room_points_dicts):
        rm_to_rm_boundary_pts.append(list(itertools.product(exits.items(), rooms.items())))

    start_points_output = {}
    x = 0
    for combo_lists in rm_to_rm_boundary_pts:

        room_door_distances = [get_segment_len(x[0][1][0], x[0][1][1], x[1][1][0], x[1][1][1]) for x in combo_lists]
        item = max(room_door_distances)

        index = room_door_distances.index(item)
        key = rm_to_rm_boundary_pts[x][index][1][0]
        val = rm_to_rm_boundary_pts[x][index][1][1]
        start_points_output.update({str(key): val})
        x +=1

    graph.add_nodes_from(start_points_output.keys())
    for n, p in start_points_output.items():
        graph.nodes[n]['pos'] = p
