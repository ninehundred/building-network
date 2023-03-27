from specklepy.api.wrapper import StreamWrapper
from specklepy.api import operations


def get_speckle_data(host: str, stream_id: str, commit_id: str):
    wrapper = StreamWrapper(f"https://{host}/streams/{stream_id}/commits/{commit_id}")

    # get an authenticated SpeckleClient if you have a local account for the server
    client = wrapper.get_client()

    # get an authenticated ServerTransport if you have a local account for the server
    transport = wrapper.get_transport()
    commit = client.commit.get(stream_id, commit_id)
    return operations.receive(commit.referencedObject, transport)
