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

    building_01_obj = Building()
    speckle_data_handler = SpeckleDataHandler(data)

    # TODO: need to build a data checker that reviews if all params and properties are present and exits if not
    speckle_data_handler.process_levels(building_01_obj)

    # TODO: ensure the rooms and doors are then placed on levels

    # XXX: will the below look more like speckle_data_handler.levels.process_rooms(level)
    #  will probably have to iterate over the levels and then process the associated
    speckle_data_handler.process_rooms(building_01_obj)

    # speckle_data_handler.process_doors(building_01_obj)

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
