import os
import pickle

from lib.build_network.BuildNetwork import BuildNetwork
from lib.utils.download_data import load_local_data
from lib.models.Building import Building
from lib.utils.SpeckleDataHandler import SpeckleDataHandler


def main():
<<<<<<< HEAD
    print(os.listdir())
    with open(r"_archive\pickles_and_hard_data\building_data.pkl", 'rb') as read:
        data = pickle.load(read)
    # data = load_local_data("building_data.pkl")
=======
    data = load_local_data(r"building_data.pkl")
>>>>>>> 4db7886a027be65abe4760a95c79d9fa1c33d4d7
    building = Building()

    spek = SpeckleDataHandler(data)
    spek.process_rooms(building)
    spek.process_doors(building)

    bn = BuildNetwork(building=building, level="02")
    bn.add_door_centroids()
    bn.add_room_coordinates()
    bn.compute_all_edges()
    bn.remove_intersecting_edges()
    bn.add_room_centroids()
    bn.plot_all_paths(normalise=25)
    # bn.plot_single_path(normalise=25, start_node_index=1)
    return


if __name__ == "__main__":
    main()
