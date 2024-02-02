import networkx as nx


class network:
    def __init__(self):
        self.distance = [200, 300, 400, 500, 600, 700, 600, 500, 400, 300, 200]
        self.topology = self.get_topology()

    def get_topology(self):
        G = nx.Graph()

        G.add_node(1)
        G.add_node(2)
        G.add_node(3)
        G.add_node(4)
        G.add_node(5)
        G.add_node(6)
        G.add_node(7)

        G.add_edge(1, 7, distance=self.distance[0], occupied=False, free_capacity=400, occupied_capacity=0, channels=96,
                   occupied_channel=0, occupied_requests=[])
        G.add_edge(1, 2, distance=self.distance[1], occupied=False, free_capacity=400, occupied_capacity=0, channels=96,
                   occupied_channel=0, occupied_requests=[])
        G.add_edge(6, 7, distance=self.distance[2], occupied=False, free_capacity=400, occupied_capacity=0, channels=96,
                   occupied_channel=0, occupied_requests=[])
        G.add_edge(2, 7, distance=self.distance[3], occupied=False, free_capacity=400, occupied_capacity=0, channels=96,
                   occupied_channel=0, occupied_requests=[])
        G.add_edge(2, 6, distance=self.distance[4], occupied=False, free_capacity=400, occupied_capacity=0, channels=96,
                   occupied_channel=0, occupied_requests=[])
        G.add_edge(2, 3, distance=self.distance[5], occupied=False, free_capacity=400, occupied_capacity=0, channels=96,
                   occupied_channel=0, occupied_requests=[])
        G.add_edge(3, 6, distance=self.distance[6], occupied=False, free_capacity=400, occupied_capacity=0, channels=96,
                   occupied_channel=0, occupied_requests=[])
        G.add_edge(3, 4, distance=self.distance[7], occupied=False, free_capacity=400, occupied_capacity=0, channels=96,
                   occupied_channel=0, occupied_requests=[])
        G.add_edge(4, 6, distance=self.distance[8], occupied=False, free_capacity=400, occupied_capacity=0, channels=96,
                   occupied_channel=0, occupied_requests=[])
        G.add_edge(4, 5, distance=self.distance[9], occupied=False, free_capacity=400, occupied_capacity=0, channels=96,
                   occupied_channel=0, occupied_requests=[])
        G.add_edge(5, 6, distance=self.distance[10], occupied=False, free_capacity=400, occupied_capacity=0, channels=96,
                   occupied_channel=0, occupied_requests=[])

        return G
