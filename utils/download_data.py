from speckle.speckle import get_speckle_data
import pickle

host = "v2.speckle.arup.com"
stream_id = "32f492d9ac"
commit_id = "ea1995828f"


def download_data(host: str, stream_id: str, commit_id: str, filename: str='building_data.pkl', path: str= ''):
    res = get_speckle_data(host, stream_id, commit_id)
    with open(path + filename, 'wb') as outp:
        pickle.dump(res, outp, pickle.HIGHEST_PROTOCOL)


def load_local_data(filename: str='building_data.pkl', path=''):
    with open(path + filename, 'rb') as inp:
        data = pickle.load(inp)
    return data


def test():
    download_data(host, stream_id, commit_id)
    data = load_local_data()
    print(data)


if __name__ == '__main__':
    test()
