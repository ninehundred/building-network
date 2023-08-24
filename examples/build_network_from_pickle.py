import os
import pickle

from lib.build_network.BuildNetwork import BuildNetwork
from lib.utils.download_data import load_local_data
from lib.models.Building import Building
from lib.utils.SpeckleDataHandler import SpeckleDataHandler


def main():
    # print(os.listdir())
    with open(r"examples\building_data.pkl", 'rb') as read:
        data = pickle.load(read)

    # Create a building object class with all required data
    building_01_obj = Building()
    speckle_data_handler = SpeckleDataHandler(data)
    speckle_data_handler.process_levels(building_01_obj)
    speckle_data_handler.process_rooms(building_01_obj)
    speckle_data_handler.process_doors(building_01_obj)

    # XXX: might start looking a bit different from here as the level will need to be an ID.
    # XXX: may have to start looking into a basic front end here to display all level info in drop down menu or something

    # building_network = BuildNetwork(building=building, level="02")
    # building_network.add_door_centroids()
    # building_network.add_room_coordinates()
    # building_network.compute_all_edges()
    # building_network.remove_intersecting_edges()
    # building_network.add_room_centroids()
    # building_network.plot_all_paths(normalise=25)
    # building_network.plot_single_path(normalise=25, start_node_index=1)
    return


if __name__ == "__main__":
    main()
