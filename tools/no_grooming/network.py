import networkx as nx
import uuid




class National_network:
    def __init__(self):
        self.distance = [200, 300, 400, 500, 600, 700, 600, 500, 400, 300, 200]
        self.topology = self.get_topology()

    def get_topology(self):
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


class Continental_network:
    def __init__(self):
        self.topology = self.get_topology()

    def get_topology(self):
        G = nx.MultiGraph()

        G.add_edge(1, 7, distance=259, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(1, 12, distance=1067, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(1, 13, distance=552, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(1, 14, distance=540, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(2, 4, distance=1209, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(2, 22, distance=1500, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(3, 15, distance=796, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(3, 16, distance=760, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(4, 8, distance=474, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(4, 27, distance=551, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(5, 9, distance=540, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(5, 13, distance=381, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(5, 18, distance=757, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(5, 21, distance=420, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(5, 26, distance=775, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(6, 16, distance=834, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(6, 20, distance=747, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(7, 11, distance=474, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(7, 20, distance=393, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(8, 21, distance=668, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(8, 26, distance=819, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(9, 19, distance=772, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(10, 12, distance=462, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(10, 14, distance=690, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(11, 13, distance=592, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(11, 19, distance=456, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(11, 24, distance=271, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(14, 20, distance=514, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(15, 20, distance=594, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(15, 28, distance=507, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(17, 18, distance=522, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(17, 22, distance=720, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(17, 28, distance=327, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(18, 25, distance=534, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(19, 23, distance=623, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(20, 24, distance=600, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(21, 25, distance=376, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(22, 27, distance=783, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(23, 26, distance=1213, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(24, 28, distance=218, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)
        G.add_edge(25, 27, distance=400, occupied=False, free_capacity=400, occupied_capacity=0, channels=192,
                   occupied_channel=0, occupied_requests=[], step=1, type='fiber', key=uuid.uuid4().hex)

        return G