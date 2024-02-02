import os
import networkx as nx
import random
import matplotlib.pyplot as plt
import heapq
import math
import collections

ZR_REACH_TABLE = {"16QAM": {"rate": 400, "channel": 75, "reach": 600},
                  "8QAM": {"rate": 300, "channel": 75, "reach": 1800},
                  "QPSK_1": {"rate": 200, "channel": 75, "reach": 3000},
                  "QPSK_2": {"rate": 100, "channel": 50, "reach": 3000}}

OEO_REACH_TABLE = {"PCS64QAM_1": {"rate": 800, "channel": 100, "reach": 150},
                   "PCS64QAM_2": {"rate": 700, "channel": 100, "reach": 400},
                   "16QAM_1": {"rate": 600, "channel": 100, "reach": 700},
                   "PCS16QAM_1": {"rate": 500, "channel": 100, "reach": 1300},
                   "PCS16QAM_2": {"rate": 400, "channel": 100, "reach": 2500},
                   "PCS16QAM_3": {"rate": 300, "channel": 100, "reach": 4700},
                   "64QAM": {"rate": 300, "channel": 50, "reach": 100},
                   "16QAM_2": {"rate": 200, "channel": 50, "reach": 900},
                   "QPSK": {"rate": 100, "channel": 50, "reach": 3000}}

OEO_ZR_REACH_TABLE = {"PCS64QAM_1": {"rate": 800, "channel": 100, "reach": 150},
                      "PCS64QAM_2": {"rate": 700, "channel": 100, "reach": 400},
                      "16QAM_1": {"rate": 600, "channel": 100, "reach": 700},
                      "PCS16QAM_1": {"rate": 500, "channel": 100, "reach": 1300},
                      "PCS16QAM_2": {"rate": 400, "channel": 100, "reach": 2500},
                      "PCS16QAM_3": {"rate": 300, "channel": 100, "reach": 4700},
                      "64QAM": {"rate": 300, "channel": 50, "reach": 100},
                      "16QAM_2": {"rate": 200, "channel": 50, "reach": 900},
                      "QPSK_3": {"rate": 100, "channel": 50, "reach": 3000},
                      "16QAM_3": {"rate": 400, "channel": 75, "reach": 600},
                      "8QAM": {"rate": 300, "channel": 75, "reach": 1800},
                      "QPSK_1": {"rate": 200, "channel": 75, "reach": 3000},
                      "QPSK_2": {"rate": 100, "channel": 50, "reach": 3000}}


def gen_request(num):
    rate_list = [100, 200, 300, 400]
    request = []
    for i in range(0, num):
        src, dst = random.sample(range(1, 8), 2)
        rate = random.sample(range(0, 4), 1)[0]

        request.append((src, dst, rate_list[rate], i + 1))

    return request


def generate_resource_graph(network):
    G = nx.Graph()
    for u, v, data in network.topology.edges(data=True):
        if data['occupied_channel'] == 96:
            continue
        else:
            G.add_edge(u, v, **data)
    return G


def link_is_available(modulation, edge_data):
    for num, mod in enumerate(modulation):
        if edge_data['distance'] <= modulation[mod]['reach'] and edge_data['channels'] >= math.ceil(modulation[mod][
                                                                                                        'channel'] / 50):
            return True

    return False


def find_shortest_path_ZR(request, network):
    # request[source, destination, rate, id]
    requests = {"source": request[0], "destination": request[1], "rate": request[2], "id": request[3]}
    modulation = {}
    for num, mod in enumerate(ZR_REACH_TABLE):
        if ZR_REACH_TABLE[mod]['rate'] == requests['rate']:
            modulation[mod] = ZR_REACH_TABLE[mod]
    G = generate_resource_graph(network)
    start = requests["source"]
    end = requests["destination"]
    # modified dijkstra
    distances = {node: float('infinity') for node in G.nodes}
    previous_nodes = {node: None for node in G.nodes}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end:
            break

        if current_node not in G:
            print(f"Node {current_node} is not in the graph.")
            return [], modulation


        for neighbor in G.neighbors(current_node):
            edge_data = G.get_edge_data(current_node, neighbor)
            tentative_distance = current_distance + edge_data['distance']
            if link_is_available(modulation, edge_data):
                if tentative_distance < distances[neighbor]:
                    distances[neighbor] = tentative_distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (tentative_distance, neighbor))

    path = []
    current_node = end
    if current_node in previous_nodes and previous_nodes[current_node] is not None:
        while current_node is not None:
            path.insert(0, current_node)
            current_node = previous_nodes.get(current_node, None)
        return path, modulation
    else:
        print(f"No path found from node {start} to node {end}")
        return [], modulation





def build_distance(path, network):
    distance_table = {}
    G = network.topology
    for i in range(len(path) - 1):
        distance_table[path[i]] = {}
        cumulative_distance = 0
        for j in range(i + 1, len(path)):
            cumulative_distance += G[path[j - 1]][path[j]]['distance']
            distance_table[path[i]][path[j]] = cumulative_distance
    return distance_table


def compute_cost_ZR(path, modulation, network):
    distance_table = build_distance(path, network)
    mod = list(modulation.keys())[0]
    num_ZR = 2
    i = 0
    while i < len(path) - 1:
        for j in range(i + 1, len(path)):
            if distance_table[path[i]][path[j]] > modulation[mod]['reach']:
                num_ZR += 2
                i = j - 1
                break
        i += 1
    print(path, num_ZR)
    print(distance_table)
    print(modulation)
    power = 6 * num_ZR
    return power



