import networkx as nx
import uuid

def get_topology():
    G = nx.MultiGraph()

    G.add_edge(1, 7, distance=306, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(1, 8, distance=298, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(1, 11, distance=174, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(2, 7, distance=114, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(2, 8, distance=120, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(2, 14, distance=144, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(3, 5, distance=37, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(3, 8, distance=208, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(3, 10, distance=88, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(3, 14, distance=278, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(4, 5, distance=36, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(4, 10, distance=41, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(6, 8, distance=316, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(6, 10, distance=182, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(6, 11, distance=400, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(6, 12, distance=85, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(6, 15, distance=224, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(7, 8, distance=157, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(8, 11, distance=258, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(9, 12, distance=64, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(9, 16, distance=74, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(11, 15, distance=275, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(13, 15, distance=179, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(13, 17, distance=143, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(15, 16, distance=187, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
    G.add_edge(16, 17, distance=86, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
               occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)

    return G


class network:
    def __init__(self):
        self.distance = [200, 300, 400, 500, 600, 700, 600, 500, 400, 300, 200]
        self.topology = get_topology()
