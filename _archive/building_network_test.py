from BuildNetwork import BuildNetwork
from _archive.download_data import load_local_data
from models.Building import Building
from utils.SpeckleDataHandler import SpeckleDataHandler


def main():
    data = load_local_data("building_data.pkl")
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
    bn.plot_all_paths()

    return


if __name__ == "__main__":
    main()
